import numpy as np
import matplotlib.pyplot as plt
from astroquery.vizier import Vizier
from astropy.coordinates import SkyCoord
import astropy.units as u
from scipy.spatial import KDTree

# --- 1. CONFIGURATION ---
# Querying a larger 20k sample for robust binning
v = Vizier(columns=['*'], row_limit=20000)

def run_oglr_v2_binned_test():
    print("Initiating final binned check on DESI DR1...")
    coord = SkyCoord(ra=180.0, dec=30.0, unit=(u.deg, u.deg), frame='icrs')
    
    try:
        # Use the spectroscopic redshift catalog
        result = v.query_region(coord, radius=2.0*u.deg, catalog=["V/161/zpix"])
        if not result: result = v.query_region(coord, radius=2.0*u.deg, catalog=["V/161"])
        
        table = result[0]
        # Column mapping
        ra = np.array(table[[c for c in table.colnames if 'RA' in c.upper()][0]])
        dec = np.array(table[[c for c in table.colnames if 'DE' in c.upper()][0]])
        z = np.array(table[[c for c in table.colnames if c.lower() == 'z' or 'z_phot' in c.lower()][0]])

        # --- 2. ΩGLR v2 PHYSICS ---
        kappa = 50.0  # Transition sharpness
        alpha = 1/3   # Relaxation suppression
        
        # Stability Metric R(t) Proxy
        tree = KDTree(np.column_stack((ra, dec)))
        densities = tree.query_ball_point(np.column_stack((ra, dec)), r=0.04, return_length=True)
        r_ratios = densities / np.percentile(densities, 85)

        # REDSHIFT BINS
        # High-z (Early), Mid-z, Low-z (Late)
        bins = [(0.8, 1.2, 'Early Universe (Stiff)', 'purple'), 
                (0.5, 0.8, 'Middle Epoch (Softening)', 'orange'), 
                (0.1, 0.5, 'Late Universe (Thawing)', 'cyan')]

        plt.figure(figsize=(10, 6))
        
        for z_min, z_max, label, color in bins:
            mask = (z >= z_min) & (z < z_max)
            bin_r = r_ratios[mask]
            
            if len(bin_r) == 0: continue
            
            # Apply Bekenstein Trigger
            logistic_term = 1.0 / (1.0 + np.exp(-kappa * (bin_r - 1.0)))
            e_mod = np.exp(-1.0 * logistic_term)
            w_pred = -1.0 + (alpha * (1 - e_mod))
            
            # Use scatter to show individual points in each bin
            plt.scatter(bin_r, w_pred, label=label, color=color, s=5, alpha=0.6)

        # --- 3. FINAL POLISH ---
        plt.axhline(-1, color='green', linestyle='--', label=r'$\Lambda$CDM ($w=-1$)')
        plt.axvline(1.0, color='red', linestyle=':', label='Bekenstein Bound')
        
        plt.title(r'Redshift-Binned $\Omega$GLR Analysis: Environmental Thawing')
        plt.xlabel(r'Local Stability Ratio ($R/S_{max}$)')
        plt.ylabel(r'Predicted Equation of State ($w$)')
        plt.legend()
        plt.grid(alpha=0.3)
        plt.show()

    except Exception as e:
        print(f"Binned analysis failed: {e}")

if __name__ == "__main__":
    run_oglr_v2_binned_test()