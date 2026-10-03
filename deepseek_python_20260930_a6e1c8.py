"""
ZypyZape vs BESS vs SyncCond — Gemelos digitales + análisis económico
Víctor Manzanares Alberola / EPSA-UPV · versión corregida
"""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ═══════════════════════════════════════════════════════════════════
# 1. PARÁMETROS DE RED Y ESCENARIO
# ═══════════════════════════════════════════════════════════════════
S_base   = 2.0e9       # 2 GW
f0       = 50.0
H_sys    = 4.0         # s
D_amort  = 0.05        # pu
T_gov    = 5.0
R_droop  = 0.05
P_gov_max = 0.15 * S_base

dt       = 0.05
t_max    = 120.0
t_pert   = 30.0
time     = np.arange(0, t_max, dt)
N        = len(time)

# ═══════════════════════════════════════════════════════════════════
# 2. MODELOS DE LOS 4 GEMELOS
# ═══════════════════════════════════════════════════════════════════

# --- Parámetros ZypyZape (del repo) ---
N_TURB   = 10           # turbinas por módulo
S_TURB   = 2.5e6        # 2.5 MW por turbina
J_TURB   = 5.0e6        # kg·m²
OM_RATED = 1.2          # rad/s
H_ZZ_MOD = 0.5 * N_TURB * J_TURB * OM_RATED**2 / (N_TURB * S_TURB)  # H por turbina
P_ZZ_NOM = 0.13 * N_TURB * S_TURB  # 13% de S_NOM como máximo intercambio

# --- Quijote (parámetros v4.7) ---
N_BLADES = 3
M_Q      = 4.0          # kg/pala
R_Q_MIN  = 5.0
R_Q_MAX  = 55.0
V_SLIDE  = 0.5          # m/s
N_Q      = 5            # turbinas equipadas

def J_quijote(r):
    return J_TURB + N_BLADES * M_Q * r * r

def bess_response(f, dfdt, soc, P_prev, P_rated=25e6, C_rate=0.5):
    """BESS: responde a desviación de frecuencia, limitado por SOC y C-rate."""
    # Respuesta tipo droop+inercia
    P_target = -8.0 * (dfdt / f0) * P_rated - 4.0 * ((f - f0) / f0) * P_rated
    P_target = np.clip(P_target, -P_rated, P_rated)
    # Límite de SOC
    if soc <= 0.05 and P_target > 0:  P_target = 0
    if soc >= 0.95 and P_target < 0:  P_target = 0
    return P_target

def zz_fw_response(f, dfdt):
    """ZypyZape FW: inercia virtual desde rotores existentes. Sin hardware."""
    # P_inj = -2·H_zz·S·(df/dt)/f0
    H_zz = N_TURB * H_ZZ_MOD
    P = -2.0 * H_zz * (N_TURB * S_TURB) * (dfdt / f0)
    return np.clip(P, -P_ZZ_NOM, P_ZZ_NOM)

def zz_quijote_response(f, dfdt, r_q_state):
    """ZypyZape + Quijote: J(t) variable con dJ/dt real."""
    # Controlador Quijote (simplificado del repo)
    vs = np.clip(8.0 * (OM_RATED - 1.2) + 4.0 * (f - f0), -V_SLIDE, V_SLIDE)
    # Actualiza r_q
    r_q_state[:N_Q] = np.clip(r_q_state[:N_Q] + vs * dt, R_Q_MIN, R_Q_MAX)
    # J y dJ/dt para cada turbina con Quijote
    J_arr = np.array([J_quijote(r_q_state[i]) if i < N_Q else J_TURB
                      for i in range(N_TURB)])
    dJdt_arr = np.array([N_BLADES * M_Q * 2.0 * r_q_state[i] * vs if i < N_Q else 0.0
                         for i in range(N_TURB)])
    # P_inertia = -Σ(J_i·ω·dω/dt + ½·dJ_i/dt·ω²)
    # El segundo término es el "bonus Quijote"
    P = -np.sum(dJdt_arr) * 0.5 * OM_RATED**2
    return np.clip(P, -P_ZZ_NOM * 2, P_ZZ_NOM * 2), r_q_state

def sync_cond_response(f, dfdt, H_sc=2.0, S_sc=100e6):
    """Condensador síncrono: inercia pura."""
    P = -2.0 * H_sc * S_sc * (dfdt / f0)
    return P

# ═══════════════════════════════════════════════════════════════════
# 3. BUCLE DE SIMULACIÓN
# ═══════════════════════════════════════════════════════════════════

def simulate(twin, dP_event=-100e6):
    f     = np.zeros(N); f[0] = f0
    dfdt  = np.zeros(N)
    P_gov = np.zeros(N)
    P_inj = np.zeros(N)
    soc   = 0.5
    r_q   = np.full(N_TURB, (R_Q_MIN + R_Q_MAX) / 2.0)

    H_eq = H_sys
    if twin == 'ZZ_FW':      H_eq = H_sys + N_TURB * H_ZZ_MOD / 10.0
    if twin == 'ZZ_Quijote': H_eq = H_sys + N_TURB * H_ZZ_MOD / 10.0
    if twin == 'SyncCond':   H_eq = H_sys + 0.1  # 100 MVA sobre 2 GW

    for i in range(1, N):
        t = time[i]
        # Gobernador
        df = f[i-1] - f0
        P_gov_target = np.clip(-(df / (R_droop * f0)) * S_base, 0, P_gov_max)
        P_gov[i] = P_gov[i-1] + (P_gov_target - P_gov[i-1]) / T_gov * dt

        # Respuesta de cada tecnología
        if twin == 'BESS':
            P_inj[i] = bess_response(f[i-1], dfdt[i-1], soc, P_inj[i-1])
            # Actualizar SOC
            soc -= P_inj[i] * dt / (2e6 * 3600)  # 2 MWh
            soc = np.clip(soc, 0, 1)
        elif twin == 'ZZ_FW':
            P_inj[i] = zz_fw_response(f[i-1], dfdt[i-1])
        elif twin == 'ZZ_Quijote':
            P_inj[i], r_q = zz_quijote_response(f[i-1], dfdt[i-1], r_q)
        elif twin == 'SyncCond':
            P_inj[i] = sync_cond_response(f[i-1], dfdt[i-1])

        # ═══ ECUACIÓN DE SWING CORREGIDA ═══
        # 2H/f0 · df/dt = (Pm - Pe) / S  →  df/dt = (ΔP + P_gov + P_inj - D·S·(f-f0))·f0/(2H·S)
        dP_step = dP_event if t >= t_pert else 0.0
        imbalance = dP_step + P_gov[i] + P_inj[i] - D_amort * S_base * (f[i-1] - f0) / f0
        dfdt[i] = imbalance * f0 / (2.0 * H_eq * S_base)
        f[i] = f[i-1] + dfdt[i] * dt

    # Métricas
    idx_pert = int(t_pert / dt)
    f_nadir = float(np.min(f[idx_pert:]))
    rocof_max = float(np.max(np.abs(dfdt[idx_pert:idx_pert+20])))
    # Recuperación a 49.9 Hz
    t_rec = t_max
    for j in range(idx_pert, N):
        if f[j] >= 49.9:
            t_rec = time[j] - t_pert
            break
    E_inj = float(np.sum(np.maximum(P_inj[idx_pert:], 0)) * dt) / 3.6e9  # MWh

    return {'f': f, 'dfdt': dfdt, 'P_inj': P_inj, 'P_gov': P_gov,
            'f_nadir': f_nadir, 'rocof_max': rocof_max,
            't_rec': t_rec, 'E_inj': E_inj, 'H_eq': H_eq}

# ═══════════════════════════════════════════════════════════════════
# 4. MONTE CARLO
# ═══════════════════════════════════════════════════════════════════
twins = ['BESS', 'ZZ_FW', 'ZZ_Quijote', 'SyncCond']
results_mc = {t: [] for t in twins}

for dP in [-50e6, -100e6, -200e6, -500e6]:
    for _ in range(25):
        for tw in twins:
            r = simulate(tw, dP_event=dP + np.random.randn() * 5e6)
            r['dP'] = dP
            results_mc[tw].append(r)

# ═══════════════════════════════════════════════════════════════════
# 5. AGREGACIÓN Y TABLA
# ═══════════════════════════════════════════════════════════════════
summary = []
for tw in twins:
    data = results_mc[tw]
    summary.append({
        'Sistema': tw,
        'f_nadir (Hz)': np.mean([r['f_nadir'] for r in data]),
        'ROCOF_max (Hz/s)': np.mean([r['rocof_max'] for r in data]),
        't_rec (s)': np.mean([r['t_rec'] for r in data]),
        'E_inj (MWh)': np.mean([r['E_inj'] for r in data]),
        'H_eq (s)': data[0]['H_eq'],
    })

df_summary = pd.DataFrame(summary)
print("\n═══ MÉTRICAS FÍSICAS ═══")
print(df_summary.to_string(index=False))

# ═══════════════════════════════════════════════════════════════════
# 6. ANÁLISIS ECONÓMICO
# ═══════════════════════════════════════════════════════════════════
WACC = 0.06
YEARS = 15
FCR = 112_000  # €/MW·año (Alemania 2023)

sist_eco = {
    'BESS':              {'capex': 1_000_000, 'opex': 20_000, 'vida': 15},
    'ZZ_FW':             {'capex':     10_000, 'opex':  2_000, 'vida': 25},
    'ZZ_Quijote':        {'capex':     40_000, 'opex':  5_000, 'vida': 20},
    'SyncCond':          {'capex':    250_000, 'opex':  5_000, 'vida': 30},
}

eco_rows = []
for name, d in sist_eco.items():
    net = FCR - d['opex']
    payback = d['capex'] / net if net > 0 else 999
    # ROI descontado a 15 años
    vpn = -d['capex']
    for y in range(1, YEARS + 1):
        vpn += net / (1 + WACC) ** y
    roi = (vpn / d['capex']) * 100
    lcos = (d['capex'] + d['opex'] * YEARS) / (FCR * YEARS / 100)  # simplificado
    eco_rows.append({
        'Sistema': name,
        'CAPEX €/MW': d['capex'],
        'OPEX €/MW·año': d['opex'],
        'Payback (años)': round(payback, 2),
        'ROI 15a (%)': round(roi, 0),
    })

df_eco = pd.DataFrame(eco_rows)
print("\n═══ MÉTRICAS ECONÓMICAS ═══")
print(df_eco.to_string(index=False))

# ═══════════════════════════════════════════════════════════════════
# 7. FIGURAS
# ═══════════════════════════════════════════════════════════════════
BG, PAN = '#0d0d1a', '#13132b'
COL = {'BESS': '#e74c3c', 'ZZ_FW': '#00d2ff',
       'ZZ_Quijote': '#2ecc71', 'SyncCond': '#f39c12'}

fig, axes = plt.subplots(2, 2, figsize=(14, 10), facecolor=BG)
axes = axes.flatten()

# Panel 1: respuesta frecuencia para cada gemelo (un caso)
for tw in twins:
    r = simulate(tw, dP_event=-100e6)
    axes[0].plot(time, r['f'], color=COL[tw], lw=2, label=tw)
axes[0].axhline(49.5, color='yellow', ls=':', lw=1, label='49.5 Hz')
axes[0].axvline(t_pert, color='white', ls='--', lw=0.8, alpha=0.5)
axes[0].set_title('Respuesta de frecuencia · ΔP = −100 MW', color='white')
axes[0].set_xlabel('t [s]', color='#aaa'); axes[0].set_ylabel('f [Hz]', color='#aaa')
axes[0].legend(fontsize=8); axes[0].grid(alpha=0.2)

# Panel 2: ROCOF vs ΔP
for tw in twins:
    dp_vals, rocof_vals = [], []
    for dP in [-50e6, -100e6, -200e6, -500e6]:
        r = simulate(tw, dP_event=dP)
        dp_vals.append(-dP/1e6); rocof_vals.append(r['rocof_max'])
    axes[1].plot(dp_vals, rocof_vals, 'o-', color=COL[tw], lw=2, label=tw)
axes[1].set_title('ROCOF máximo vs perturbación', color='white')
axes[1].set_xlabel('ΔP [MW]', color='#aaa'); axes[1].set_ylabel('|ROCOF| [Hz/s]', color='#aaa')
axes[1].legend(fontsize=8); axes[1].grid(alpha=0.2)

# Panel 3: CAPEX vs OPEX
for i, (name, d) in enumerate(sist_eco.items()):
    axes[2].bar(i - 0.2, d['capex'], 0.35, color=COL[name], label='CAPEX')
    axes[2].bar(i + 0.2, d['opex'] * 15, 0.35, color=COL[name], alpha=0.5, label='OPEX 15a')
axes[2].set_xticks(range(len(sist_eco)))
axes[2].set_xticklabels(list(sist_eco.keys()), color='#aaa', fontsize=8)
axes[2].set_yscale('log')
axes[2].set_title('CAPEX vs OPEX 15 años (€/MW, escala log)', color='white')
axes[2].set_ylabel('€/MW', color='#aaa'); axes[2].grid(alpha=0.2, axis='y')

# Panel 4: ROI 15 años
rois = [r['ROI 15a (%)'] for r in eco_rows]
names = [r['Sistema'] for r in eco_rows]
colors = [COL[n] for n in names]
axes[3].barh(names, rois, color=colors)
axes[3].set_title('ROI a 15 años con FCR = 112 k€/MW·año', color='white')
axes[3].set_xlabel('ROI [%]', color='#aaa'); axes[3].grid(alpha=0.2, axis='x')
axes[3].set_xscale('symlog')

for ax in axes:
    ax.set_facecolor(PAN)
    ax.tick_params(colors='#aaa', labelsize=8)
    for sp in ax.spines.values(): sp.set_color('#333')
    ax.title.set_color('white')

plt.tight_layout()
plt.savefig('/home/claude/zypyzape_comparativa.png', dpi=150, facecolor=BG, bbox_inches='tight')
print("\n✔ Figura: zypyzape_comparativa.png")

# ═══════════════════════════════════════════════════════════════════
# 8. EXPORTAR CSV
# ═══════════════════════════════════════════════════════════════════
df_summary.to_csv('/home/claude/metricas_fisicas.csv', index=False)
df_eco.to_csv('/home/claude/metricas_economicas.csv', index=False)
print("✔ CSV: metricas_fisicas.csv, metricas_economicas.csv")