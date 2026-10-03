"""
ZypyZape vs BESS vs SyncCond — Gemelos + análisis económico
Versión corregida · Víctor Manzanares Alberola / EPSA-UPV
"""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ═══════════════════════════════════════════════════════════════
# 1. PARÁMETROS DE RED
# ═══════════════════════════════════════════════════════════════
S_base   = 2.0e9
f0       = 50.0
H_sys    = 4.0
D_amort  = 0.05
T_gov    = 5.0
R_droop  = 0.05
P_gov_max = 0.15 * S_base
dt       = 0.05
t_max    = 120.0
t_pert   = 30.0
time     = np.arange(0, t_max, dt)
N        = len(time)

# ═══════════════════════════════════════════════════════════════
# 2. PARÁMETROS DE LOS SISTEMAS
# ═══════════════════════════════════════════════════════════════
# ZypyZape (parque de 10 turbinas × 2.5 MW = 25 MW)
N_TURB   = 10
S_TURB   = 2.5e6
S_ZZ     = N_TURB * S_TURB          # 25 MW
J_TURB   = 5.0e6
OM_RATED = 1.2
H_ZZ_TURB = 0.5 * J_TURB * OM_RATED**2 / S_TURB    # ≈ 1.44 s
H_ZZ_PARQUE = H_ZZ_TURB            # H del parque (por unidad de S_ZZ)

# Quijote (parámetros del repo v4.7)
N_BLADES = 3
M_Q      = 4.0
R_Q_MIN  = 5.0
R_Q_MAX  = 55.0
V_SLIDE  = 0.5
N_Q      = 5

# BESS
S_BESS   = 25e6                    # 25 MW agregados
E_BESS   = 50e6                    # 50 MWh (2h a potencia nominal)
EFF_RT   = 0.88                    # eficiencia round-trip
C_RATE   = 0.5

# SyncCond
S_SC     = 100e6
H_SC     = 4.0

def J_quijote(r):
    return J_TURB + N_BLADES * M_Q * r * r

# ═══════════════════════════════════════════════════════════════
# 3. FUNCIONES DE RESPUESTA DE CADA SISTEMA
# ═══════════════════════════════════════════════════════════════
def response_bess(f, dfdt, soc, P_prev):
    """BESS: droop + inercia sintética + SOC tracking."""
    P_target = -2.0 * (dfdt/f0) * S_BESS - 15.0 * ((f - f0)/f0) * S_BESS
    P_target = np.clip(P_target, -C_RATE * S_BESS * 4, C_RATE * S_BESS * 4)
    # Límite de SOC
    if soc <= 0.05 and P_target > 0:  P_target = 0
    if soc >= 0.95 and P_target < 0:  P_target = 0
    return P_target

def response_zz_fw(f, dfdt):
    """ZypyZape FW: inercia virtual del parque. SIN hardware extra.
    P_inj = -2·H_zz·S_zz·(df/dt)/f0, aplicado sobre S_ZZ (25 MW), no S_base."""
    P = -2.0 * H_ZZ_PARQUE * S_ZZ * (dfdt / f0)
    # Límite físico: no puedes extraer más del 13% de S_ZZ instantáneo
    return np.clip(P, -0.13 * S_ZZ, 0.13 * S_ZZ)

def response_zz_quijote(f, dfdt, r_q, omega_est=OM_RATED):
    """ZypyZape + Quijote: J(t) variable con término cinemático dJ/dt."""
    # Controlador Quijote: mueve masa según desviación de f y ω
    e_f = f - f0
    e_om = 0.0  # asumimos ω ≈ ω_rated en régimen
    vs = float(np.clip(4.0 * e_f - 8.0 * e_om, -V_SLIDE, V_SLIDE))
    # Actualiza posiciones radiales
    r_q[:N_Q] = np.clip(r_q[:N_Q] + vs * dt, R_Q_MIN, R_Q_MAX)
    # J y dJ/dt por turbina
    J_arr = np.array([J_quijote(r_q[i]) if i < N_Q else J_TURB
                      for i in range(N_TURB)])
    dJdt_arr = np.array([N_BLADES * M_Q * 2.0 * r_q[i] * vs if i < N_Q else 0.0
                         for i in range(N_TURB)])
    # Potencia del término inercia variable (dominante):
    # P = -Σ dJ_i/dt · ω² / 2 (término "efecto patinadora")
    P = -0.5 * np.sum(dJdt_arr) * omega_est**2
    # Añade también inercia base (mismo que FW)
    P += -2.0 * H_ZZ_PARQUE * S_ZZ * (dfdt / f0)
    return np.clip(P, -0.30 * S_ZZ, 0.30 * S_ZZ), r_q

def response_sync_cond(f, dfdt):
    """Condensador síncrono: inercia pura."""
    return -2.0 * H_SC * S_SC * (dfdt / f0)

# ═══════════════════════════════════════════════════════════════
# 4. SIMULACIÓN PRINCIPAL
# ═══════════════════════════════════════════════════════════════
def simulate(twin, dP_event=-100e6):
    f     = np.zeros(N); f[0] = f0
    dfdt  = np.zeros(N)
    P_gov = np.zeros(N)
    P_inj = np.zeros(N)
    soc   = 0.5
    r_q   = np.full(N_TURB, (R_Q_MIN + R_Q_MAX) / 2.0)

    # Inercia equivalente del sistema base
    H_eq = H_sys  # el resto va como P_inj

    for i in range(1, N):
        t = time[i]
        # Gobernador
        df = f[i-1] - f0
        P_gov_target = np.clip(-(df / (R_droop * f0)) * S_base, 0, P_gov_max)
        P_gov[i] = P_gov[i-1] + (P_gov_target - P_gov[i-1]) / T_gov * dt

        # Respuesta específica del sistema
        if twin == 'BESS':
            P_inj[i] = response_bess(f[i-1], dfdt[i-1], soc, P_inj[i-1])
            soc -= P_inj[i] * dt / E_BESS / EFF_RT if P_inj[i] > 0 else \
                   -P_inj[i] * dt * EFF_RT / E_BESS
            soc = np.clip(soc, 0, 1)
        elif twin == 'ZZ_FW':
            P_inj[i] = response_zz_fw(f[i-1], dfdt[i-1])
        elif twin == 'ZZ_Quijote':
            P_inj[i], r_q = response_zz_quijote(f[i-1], dfdt[i-1], r_q)
        elif twin == 'SyncCond':
            P_inj[i] = response_sync_cond(f[i-1], dfdt[i-1])

        # ═══ ECUACIÓN DE SWING ═══
        dP_step = dP_event if t >= t_pert else 0.0
        imbalance = dP_step + P_gov[i] + P_inj[i] - D_amort * S_base * (f[i-1] - f0) / f0
        dfdt[i] = imbalance * f0 / (2.0 * H_eq * S_base)
        f[i] = f[i-1] + dfdt[i] * dt

    # Métricas
    idx_pert = int(t_pert / dt)
    f_nadir = float(np.min(f[idx_pert:]))
    rocof_max = float(np.max(np.abs(dfdt[idx_pert:idx_pert+20])))
    t_rec = t_max
    for j in range(idx_pert, N):
        if f[j] >= 49.9:
            t_rec = time[j] - t_pert
            break
    E_inj = float(np.sum(np.maximum(P_inj[idx_pert:], 0)) * dt) / 3.6e9

    return {'f': f, 'dfdt': dfdt, 'P_inj': P_inj, 'P_gov': P_gov,
            'f_nadir': f_nadir, 'rocof_max': rocof_max,
            't_rec': t_rec, 'E_inj': E_inj}

# ═══════════════════════════════════════════════════════════════
# 5. MONTE CARLO
# ═══════════════════════════════════════════════════════════════
twins = ['BESS', 'ZZ_FW', 'ZZ_Quijote', 'SyncCond']
dP_levels = [-50e6, -100e6, -200e6, -500e6]
n_mc = 20

results = {tw: [] for tw in twins}
for dP in dP_levels:
    for _ in range(n_mc):
        dP_sim = dP + np.random.randn() * 0.05 * abs(dP)
        for tw in twins:
            r = simulate(tw, dP_event=dP_sim)
            r['dP'] = dP
            results[tw].append(r)

# ═══════════════════════════════════════════════════════════════
# 6. TABLA RESUMEN
# ═══════════════════════════════════════════════════════════════
summary = []
for tw in twins:
    data = results[tw]
    summary.append({
        'Sistema': tw,
        'f_nadir (Hz)': round(np.mean([r['f_nadir'] for r in data]), 4),
        'ROCOF_max (Hz/s)': round(np.mean([r['rocof_max'] for r in data]), 4),
        't_rec (s)': round(np.mean([r['t_rec'] for r in data]), 2),
        'E_inj (MWh)': round(np.mean([r['E_inj'] for r in data]), 3),
    })

df_summary = pd.DataFrame(summary)
print("\n═══ MÉTRICAS FÍSICAS (promedio sobre 80 eventos) ═══")
print(df_summary.to_string(index=False))

# ═══════════════════════════════════════════════════════════════
# 7. ANÁLISIS ECONÓMICO
# ═══════════════════════════════════════════════════════════════
WACC = 0.06
YEARS = 15

sist_eco = {
    'BESS':         {'capex': 1_000_000, 'opex': 20_000, 'vida': 15},
    'ZZ_FW':        {'capex':     10_000, 'opex':  2_000, 'vida': 25},
    'ZZ_Quijote':   {'capex':     40_000, 'opex':  5_000, 'vida': 20},
    'SyncCond':     {'capex':    250_000, 'opex':  5_000, 'vida': 30},
}

def roi_at_fcr(fcr_price):
    rows = []
    for name, d in sist_eco.items():
        net = fcr_price - d['opex']
        payback = d['capex'] / net if net > 0 else 999
        vpn = -d['capex']
        for y in range(1, YEARS + 1):
            vpn += net / (1 + WACC) ** y
        roi = (vpn / d['capex']) * 100
        rows.append({'Sistema': name, 'Payback (años)': round(payback, 2),
                     'ROI 15a (%)': round(roi, 0)})
    return pd.DataFrame(rows)

for fcr in [50_000, 112_000, 200_000]:
    print(f"\n═══ ECONÓMICO — FCR = {fcr:,} €/MW·año ═══")
    print(roi_at_fcr(fcr).to_string(index=False))

# ═══════════════════════════════════════════════════════════════
# 8. FIGURAS
# ═══════════════════════════════════════════════════════════════
BG, PAN = '#0d0d1a', '#13132b'
COL = {'BESS': '#e74c3c', 'ZZ_FW': '#00d2ff',
       'ZZ_Quijote': '#2ecc71', 'SyncCond': '#f39c12'}

fig, axes = plt.subplots(2, 2, figsize=(14, 10), facecolor=BG)
axes = axes.flatten()

# Panel 1: respuesta f(t) para ΔP = −100 MW
for tw in twins:
    r = simulate(tw, dP_event=-100e6)
    axes[0].plot(time, r['f'], color=COL[tw], lw=2, label=tw)
axes[0].axhline(49.5, color='yellow', ls=':', lw=1, label='49.5 Hz (protección)')
axes[0].axhline(49.9, color='orange', ls=':', lw=0.8, alpha=0.5)
axes[0].axvline(t_pert, color='white', ls='--', lw=0.8, alpha=0.4)
axes[0].set_title('Respuesta f(t) · ΔP = −100 MW', color='white')
axes[0].set_xlabel('t [s]', color='#aaa'); axes[0].set_ylabel('f [Hz]', color='#aaa')
axes[0].legend(fontsize=8); axes[0].grid(alpha=0.2)

# Panel 2: ROCOF vs ΔP
for tw in twins:
    dp_v, ro_v = [], []
    for dP in dP_levels:
        r = simulate(tw, dP_event=dP)
        dp_v.append(abs(dP)/1e6); ro_v.append(r['rocof_max'])
    axes[1].plot(dp_v, ro_v, 'o-', color=COL[tw], lw=2, label=tw)
axes[1].set_title('ROCOF máximo vs ΔP', color='white')
axes[1].set_xlabel('|ΔP| [MW]', color='#aaa'); axes[1].set_ylabel('|ROCOF| [Hz/s]', color='#aaa')
axes[1].legend(fontsize=8); axes[1].grid(alpha=0.2)

# Panel 3: CAPEX + OPEX 15 años
names = list(sist_eco.keys())
capex_v = [sist_eco[n]['capex'] for n in names]
opex15_v = [sist_eco[n]['opex'] * 15 for n in names]
x = np.arange(len(names))
axes[2].bar(x - 0.2, capex_v, 0.35, color=[COL[n] for n in names], label='CAPEX')
axes[2].bar(x + 0.2, opex15_v, 0.35, color=[COL[n] for n in names],
            alpha=0.5, label='OPEX 15 años')
axes[2].set_xticks(x); axes[2].set_xticklabels(names, color='#aaa', fontsize=8)
axes[2].set_yscale('log')
axes[2].set_title('CAPEX vs OPEX 15 años (€/MW, log)', color='white')
axes[2].legend(fontsize=8); axes[2].grid(alpha=0.2, axis='y')

# Panel 4: ROI vs precio FCR
fcr_range = np.linspace(10_000, 250_000, 100)
for n in names:
    d = sist_eco[n]
    roi_curve = []
    for fcr in fcr_range:
        net = fcr - d['opex']
        if net <= 0:
            roi_curve.append(-100)
            continue
        vpn = -d['capex']
        for y in range(1, YEARS + 1):
            vpn += net / (1 + WACC) ** y
        roi_curve.append((vpn / d['capex']) * 100)
    axes[3].plot(fcr_range / 1000, roi_curve, color=COL[n], lw=2, label=n)
axes[3].axhline(0, color='white', ls=':', lw=0.8, alpha=0.5)
axes[3].axvline(112, color='yellow', ls='--', lw=1, alpha=0.7, label='FCR Alemania 2023')
axes[3].set_title('ROI a 15 años vs precio FCR', color='white')
axes[3].set_xlabel('FCR [k€/MW·año]', color='#aaa'); axes[3].set_ylabel('ROI 15a [%]', color='#aaa')
axes[3].set_yscale('symlog'); axes[3].legend(fontsize=8); axes[3].grid(alpha=0.2)

for ax in axes:
    ax.set_facecolor(PAN); ax.tick_params(colors='#aaa', labelsize=8)
    for sp in ax.spines.values(): sp.set_color('#333')
    ax.title.set_color('white')

plt.tight_layout()
plt.savefig('zypyzape_twins_comparativa.png', dpi=150, facecolor=BG, bbox_inches='tight')
print("\n✔ Figura: zypyzape_twins_comparativa.png")

df_summary.to_csv('metricas_fisicas.csv', index=False)
print("✔ CSV: metricas_fisicas.csv")