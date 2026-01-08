import pandas as pd
import os

def load_data(filepath):
    """
    Loads sieve analysis data from a CSV file.
    
    Expected columns: 'sieve_size', 'weight_retained'
    
    Args:
        filepath (str): Path to the CSV file.
        
    Returns:
        pd.DataFrame: DataFrame containing the sieve analysis data.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    try:
        df = pd.read_csv(filepath)
        required_columns = ['sieve_size', 'weight_retained']
        if not all(col in df.columns for col in required_columns):
             raise ValueError(f"CSV must contain columns: {required_columns}")
        return df
    except Exception as e:
        raise Exception(f"Error loading data: {e}")
