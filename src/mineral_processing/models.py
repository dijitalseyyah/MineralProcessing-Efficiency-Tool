import numpy as np
from scipy.optimize import curve_fit

class GaudinSchuhmann:
    """
    Gaudin-Schuhmann distribution model.
    Equation: Y = 100 * (x / k) ** m
    where:
    Y = Cumulative passing percentage
    x = Particle size
    k = Size modulus (theoretical size where 100% passes)
    m = Distribution modulus
    """
    def __init__(self):
        self.k = None
        self.m = None

    def fit(self, sizes, passing_percentages):
        """
        Fits the Gaudin-Schuhmann model to the data.
        """
        # Avoid log(0) or division by zero
        valid_indices = (sizes > 0) & (passing_percentages > 0)
        x_data = sizes[valid_indices]
        y_data = passing_percentages[valid_indices]

        # Linearize: log(Y/100) = m * log(x) - m * log(k)
        # Y_lin = m * X_lin + C
        # where Y_lin = log(Y/100), X_lin = log(x), C = -m * log(k)
        
        log_x = np.log10(x_data)
        log_y = np.log10(y_data / 100.0)

        # Fit linear model
        coeffs = np.polyfit(log_x, log_y, 1)
        self.m = coeffs[0]
        intercept = coeffs[1]
        self.k = 10 ** (-intercept / self.m)

    def predict(self, size):
        """
        Predicts cumulative passing percentage for a given size.
        """
        if self.k is None or self.m is None:
            raise ValueError("Model not fitted yet.")
        return 100 * (size / self.k) ** self.m

class RosinRammler:
    """
    Rosin-Rammler (Weibull) distribution model.
    Equation: Y = 100 * (1 - exp(-(x / d_char) ** n))
    where:
    Y = Cumulative passing percentage
    x = Particle size
    d_char = Characteristic particle size (size at which ~63.2% passes)
    n = Distribution coefficient (uniformity constant)
    """
    def __init__(self):
        self.n = None
        self.d_char = None

    def fit(self, sizes, passing_percentages):
        """
        Fits the Rosin-Rammler model to the data.
        """
         # Avoid log(0) or division by zero
        valid_indices = (sizes > 0) & (passing_percentages > 0) & (passing_percentages < 100)
        x_data = sizes[valid_indices]
        y_data = passing_percentages[valid_indices]

        # Linearize: ln(-ln(1 - Y/100)) = n * ln(x) - n * ln(d_char)
        # Y_lin = n * X_lin + C
        
        log_x = np.log(x_data)
        Y_val = -np.log(1 - y_data / 100.0)
        log_log_y = np.log(Y_val)

        coeffs = np.polyfit(log_x, log_log_y, 1)
        self.n = coeffs[0]
        intercept = coeffs[1]
        self.d_char = np.exp(-intercept / self.n)

    def predict(self, size):
        """
        Predicts cumulative passing percentage for a given size.
        """
        if self.n is None or self.d_char is None:
             raise ValueError("Model not fitted yet.")
        return 100 * (1 - np.exp(-(size / self.d_char) ** self.n))
