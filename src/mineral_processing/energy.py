import math

def calculate_bond_work_index(energy_consumption, throughput, F80, P80):
    """
    Calculates the Bond Work Index (Wi) from operational data.
    
    Wi = W / (10 * (1/sqrt(P80) - 1/sqrt(F80)))
    
    Args:
        energy_consumption (float): Energy consumption in kWh/t.
        throughput (float): Throughput in t/h (not directly used in basic formula but kept for API consistency if needed later).
        F80 (float): 80% passing size of feed in micrometers.
        P80 (float): 80% passing size of product in micrometers.
        
    Returns:
        float: Bond Work Index (kWh/t).
    """
    # Verify inputs are valid
    if F80 <= 0 or P80 <= 0:
        raise ValueError("F80 and P80 must be positive.")
    if F80 <= P80:
         raise ValueError("Feed size (F80) must be larger than product size (P80) for size reduction.")

    term = (10 / math.sqrt(P80)) - (10 / math.sqrt(F80))
    Wi = energy_consumption / term
    return Wi

def calculate_energy_required(Wi, F80, P80):
    """
    Calculates the energy required (W) to reduce material from F80 to P80.
    
    W = Wi * 10 * (1/sqrt(P80) - 1/sqrt(F80))
    
    Args:
        Wi (float): Bond Work Index.
        F80 (float): 80% passing size of feed in micrometers.
        P80 (float): 80% passing size of product in micrometers.
        
    Returns:
        float: Energy required (kWh/t).
    """
    if F80 <= 0 or P80 <= 0:
        raise ValueError("F80 and P80 must be positive.")
        
    term = (10 / math.sqrt(P80)) - (10 / math.sqrt(F80))
    W = Wi * term
    return W
