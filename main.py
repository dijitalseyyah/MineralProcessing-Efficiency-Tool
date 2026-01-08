import argparse
import sys
import os
import pandas as pd
import numpy as np

# Add src to path so we can import modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from mineral_processing.models import GaudinSchuhmann, RosinRammler
from mineral_processing.energy import calculate_bond_work_index, calculate_energy_required
from mineral_processing.efficiency import calculate_screen_efficiency, detect_blinding
from mineral_processing.reporting import generate_pdf_report
from mineral_processing.utils import load_data

def main():
    parser = argparse.ArgumentParser(description="Mineral Processing Efficiency Tool")
    parser.add_argument('--input', type=str, help="Path to input CSV file for Sieve Analysis")
    parser.add_argument('--demo', action='store_true', help="Run a demo with sample data")
    
    args = parser.parse_args()
    
    if args.demo:
        print("Running demo simulation...")
        # Create dummy data for demo
        data = {
            'sieve_size': [1000, 500, 250, 125, 63],
            'weight_retained': [10, 20, 30, 25, 15] 
        }
        df = pd.DataFrame(data)
        # Calculate passing
        total_weight = df['weight_retained'].sum()
        df['percent_retained'] = (df['weight_retained'] / total_weight) * 100
        df['cumulative_passing'] = 100 - df['percent_retained'].cumsum()
        
        print("Sample Data:")
        print(df)
        
        # 1. Model Fitting
        gs = GaudinSchuhmann()
        gs.fit(df['sieve_size'].values, df['cumulative_passing'].values)
        print(f"Gaudin-Schuhmann: k={gs.k:.2f}, m={gs.m:.2f}")
        
        p80_product = gs.predict(800) # Hypothetical reading
        print(f"Predicted P80 (Product): {p80_product:.2f}")

        # 2. Energy
        # Assumptions for demo
        feed_p80 = 12000 # microns
        product_p80 = 8000 # microns
        energy_cons = 1.85 # kWh/t
        
        wi = calculate_bond_work_index(energy_cons, 450, feed_p80, product_p80)
        print(f"Calculated Bond Work Index: {wi:.2f} kWh/t")
        
        # 3. Efficiency
        eff = calculate_screen_efficiency(0.8, 0.1, 0.95)
        print(f"Screen Efficiency: {eff*100:.2f}%")
        
        # 4. Report
        report_data = {
            'p80_feed': feed_p80,
            'p80_product': product_p80,
            'bond_work_index': round(wi, 2),
            'energy_consumption': energy_cons,
            'screen_efficiency': eff,
            'optimization_potential': 'High (Demo)'
        }
        generate_pdf_report(report_data, "demo_report.pdf")
        
    elif args.input:
        try:
            df = load_data(args.input)
            # Logic similar to demo but with real data...
            # For now just printing loaded data
            print(f"Loaded data from {args.input}")
            print(df.head())
        except Exception as e:
            print(f"Error: {e}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
