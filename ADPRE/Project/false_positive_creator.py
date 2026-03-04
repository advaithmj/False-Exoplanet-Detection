import numpy as np
import sys
sys.path.append('/Users/advaithjohn/Desktop/ADPRE/Code/Code_Files')

from environmental_stressors import EnvironmentalStressors
from detection_algorithms import BoxLeastSquaresDetector

class FalsePositiveCreator:
    """Creates false planet detections on real data using environmental stressors"""
    
    def __init__(self):
        self.stressors = EnvironmentalStressors()
        self.detector = BoxLeastSquaresDetector(period_min=0.5, period_max=20.0, n_periods=500)
    
    def apply_stressors_to_real_data(self, time, flux, stress_level=0.3):
        """Apply your thermal drift, radiation, etc. to real Kepler data"""
        # YOUR CODE HERE
        pass
    
    def attempt_false_detection(self, time, flux_clean):
        """Try to create a false planet on star with no planets"""
        # YOUR CODE HERE
        pass
    
    def corrupt_known_planet(self, time, flux, true_period):
        """Add stress to known planet data, see if we detect wrong period"""
        # YOUR CODE HERE
        pass
