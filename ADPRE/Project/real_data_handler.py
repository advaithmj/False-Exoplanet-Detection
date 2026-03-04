import numpy as np
import lightkurve as lk
from scipy.signal import savgol_filter

class RealDataHandler:
    """Handles downloading and preprocessing real exoplanet data from NASA"""
    
    def __init__(self):
        pass
    
    def download_planet_data(self, planet_name, mission='Kepler'):
        """Download light curve for a known planet"""
        # YOUR CODE HERE
        pass
    
    def download_no_planet_star(self, star_id, mission='Kepler'):
        """Download light curve for star with NO known planets"""
        # YOUR CODE HERE
        pass
    
    def preprocess(self, lc):
        """Remove trends, clean bad data, normalize"""
        # YOUR CODE HERE
        pass
    
    def extract_planet_parameters(self, lc, period):
        """Phase-fold and measure actual transit depth, duration"""
        # YOUR CODE HERE
        pass
