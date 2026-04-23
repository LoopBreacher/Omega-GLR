import numpy as np
from pathlib import Path

# ====================== FIRST-PRINCIPLES CONSTANTS ======================
H0 = 67.4                    # km/s/Mpc (Planck 2018 central value)
G = 6.67430e-11              # m³ kg⁻¹ s⁻²
Mpc_to_m = 3.08568e22
c = 2.99792458e8

# Critical density
H0_s = H0 * 1000 / Mpc_to_m
rho_c = 3 * H0_s**2 / (8 * np.pi * G)

# Observable universe radius (comoving particle horizon ≈ 46.5 Gly)
R_ly = 46.5e9
ly_to_m = 9.46073e15
R_m = R_ly * ly_to_m

V = (4.0/3.0) * np.pi * R_m**3
Gamma0 = rho_c * V

# ====================== OUTPUT ======================
print("🚀 ΩGLR Γ₀ Derivation from First Principles (Critical Density × Hubble Volume)")
print("=" * 75)
print(f"H0 used                  : {H0} km/s/Mpc")
print(f"ρ_c                      : {rho_c:.5e} kg/m³")
print(f"Observable radius        : {R_m:.5e} m")
print(f"Hubble volume            : {V:.5e} m³")
print(f"Derived Γ₀               : {Gamma0:.5e} kg")
print(f"Paper value              : 3.04 × 10^54 kg")
print(f"Agreement                : {abs(Gamma0 - 3.04e54) / 3.04e54 * 100:.3f} %")
print("=" * 75)
print("Γ₀ is cleanly derived — no free parameters, no fitting.")
print("This anchors the entire framework (vacuum energy, stability metric, scaffolding decay).")

out_dir = Path(".")
with open(out_dir / "oglr_gamma0_derivation.txt", "w") as f:
    f.write(str(Gamma0))
print("\n✅ Saved derivation log → oglr_gamma0_derivation.txt")