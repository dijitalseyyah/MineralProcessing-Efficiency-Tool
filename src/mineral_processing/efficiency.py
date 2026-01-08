def calculate_screen_efficiency(feed_undersize, oversize_undersize, undersize_undersize):
    """
    Calculates screen efficiency using the recovery formula.
    
    E = (c * (f - o)) / (f * (c - o))  <- Note: This is a general recovery formula, often used.
    However, standard screen efficiency is often defined as Efficiency of Undersize Recovery (Eu).
    
    Eu = (U * u) / (F * f)
    
    Where:
    F, U, O = Mass flow rates of Feed, Undersize, Oversize
    f, u, o = Fraction of material smaller than aperture in Feed, Undersize, Oversize.
    
    Using only fractions (rearranged mass balance):
    U/F = (f - o) / (u - o)
    
    So Eu = ((f - o) / (u - o)) * (u / f)
    
    Args:
        feed_undersize (float): Fraction of feed < aperture (0-1).
        oversize_undersize (float): Fraction of oversize < aperture (0-1) (Misplaced fines).
        undersize_undersize (float): Fraction of undersize < aperture (0-1) (Should be close to 1).
        
    Returns:
        float: Efficiency (0-1).
    """
    f = feed_undersize
    o = oversize_undersize
    u = undersize_undersize
    
    if u == o:
        raise ValueError("Invalid separation: undersize and oversize have same composition.")
    
    recovery = ((f - o) / (u - o)) * (u / f)
    return recovery

def detect_blinding(efficiency, threshold=0.85):
    """
    Simple check to see if efficiency is below a threshold, suggesting blinding.
    """
    if efficiency < threshold:
        return True, "Potential blinding or screen wear detected."
    return False, "Screen operating normally."
