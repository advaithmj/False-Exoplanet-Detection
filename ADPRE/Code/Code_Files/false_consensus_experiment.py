import numpy as np
import matplotlib.pyplot as plt
from detection_algorithms import BoxLeastSquaresDetector
from environmental_stressors import EnvironmentalStressors

class FalseConsensusExperiment:
    """
    Investigates false consensus in exoplanet detection under environmental stress
    """
    
    def __init__(self, n_detectors=5, observation_duration=50, cadence=0.04167):
        """
        Initialize the experiment
        
        Parameters:
        - n_detectors: number of independent virtual detectors
        - observation_duration: total observation time (days)
        - cadence: time between measurements (days, 0.04167 = 1 hour)
        """
        self.n_detectors = n_detectors
        self.observation_duration = observation_duration
        self.cadence = cadence
        self.time = np.arange(0, observation_duration, cadence)
        
        print("=" * 70)
        print("FALSE CONSENSUS EXPERIMENT INITIALIZED")
        print("=" * 70)
        print(f"Number of detectors: {n_detectors}")
        print(f"Observation duration: {observation_duration} days")
        print(f"Cadence: {cadence * 24:.1f} hours")
        print(f"Total observations: {len(self.time)}")
        print("=" * 70)
    
    
    def generate_planet_signal(self, period=5.0, planet_radius_ratio=0.15, 
                               transit_duration=0.15):
        """
        Generate a clean exoplanet transit signal
        
        Returns:
        - flux: clean transit signal
        - params: true planet parameters
        """
        flux = np.ones(len(self.time))
        
        # Calculate transits
        phase = (self.time % period) / period
        transit_fraction = transit_duration / period
        
        for i, p in enumerate(phase):
            if p < transit_fraction:
                normalized_pos = abs(2 * p / transit_fraction - 1)
                if normalized_pos < 1:
                    if normalized_pos < (1 - planet_radius_ratio):
                        blocked_area = planet_radius_ratio**2
                    else:
                        overlap_fraction = (1 - normalized_pos) / planet_radius_ratio
                        overlap_fraction = max(0, min(1, overlap_fraction))
                        blocked_area = planet_radius_ratio**2 * overlap_fraction
                    flux[i] = 1.0 - blocked_area
        
        params = {
            'period': period,
            'planet_radius_ratio': planet_radius_ratio,
            'transit_depth': planet_radius_ratio**2,
            'transit_duration': transit_duration
        }
        
        return flux, params
    
    
    def apply_stress(self, flux, stress_level=0.0):
        """
        Apply environmental stressors at specified level
        
        Parameters:
        - flux: clean signal
        - stress_level: 0.0 = none, 1.0 = severe (scales all stressors)
        
        Returns:
        - corrupted_flux: signal with stressors applied
        - corrupted_time: time array with jitter
        """
        corrupted_flux = flux.copy()
        
        # Scale stressor parameters by stress_level
        # Thermal drift
        drift = EnvironmentalStressors.thermal_drift(
            self.time, 
            drift_rate=0.1 + 0.2 * stress_level,
            drift_amplitude=0.003 * (1 + 3 * stress_level)
        )
        corrupted_flux += drift
        
        # Radiation noise
        radiation = EnvironmentalStressors.radiation_noise(
            self.time,
            intensity=0.005 * (1 + 5 * stress_level),
            cluster_size=int(3 + 5 * stress_level)
        )
        corrupted_flux += radiation
        
        # Signal attenuation
        corrupted_flux = EnvironmentalStressors.signal_attenuation(
            self.time,
            corrupted_flux,
            attenuation_rate=0.05 * (1 + 5 * stress_level)
        )
        
        # Timing jitter
        corrupted_time = EnvironmentalStressors.timing_jitter(
            self.time,
            jitter_amplitude=0.0005 * (1 + 4 * stress_level)
        )
        
        return corrupted_flux, corrupted_time
    
    
    def simulate_detector_observations(self, flux, n_detectors, detector_noise=0.002):
        """
        Simulate multiple independent detectors observing the same signal
        
        Each detector has independent noise but sees the SAME environmental stress
        (this is the key to false consensus)
        
        Returns:
        - observations: list of flux arrays, one per detector
        """
        observations = []
        
        for detector_id in range(n_detectors):
            # Each detector has independent stellar/instrumental noise
            np.random.seed(detector_id + 100)
            noise = np.random.normal(0, detector_noise, len(flux))
            
            detector_flux = flux + noise
            observations.append(detector_flux)
        
        return observations
    
    
    def run_single_trial(self, stress_level, true_period):
        """
        Run one experimental trial at a given stress level
        
        Returns:
        - results: detection results from all detectors
        """
        # Generate clean signal
        flux_clean, params = self.generate_planet_signal(period=true_period)
        
        # Apply shared environmental stress
        flux_stressed, time_stressed = self.apply_stress(flux_clean, stress_level)
        
        # Simulate multiple detector observations
        observations = self.simulate_detector_observations(flux_stressed, self.n_detectors)
        
        # Run detection on each observation
        detector = BoxLeastSquaresDetector(period_min=3.0, period_max=7.0, n_periods=400)
        
        results = []
        for i, obs in enumerate(observations):
            detected, det_results = detector.detect(time_stressed, obs, threshold=3.0)
            
            # Store results
            results.append({
                'detector_id': i,
                'detected': detected,
                'best_period': det_results['best_period'],
                'power': det_results['power'],
                'confidence': det_results['confidence'],
                'period_error': abs(det_results['best_period'] - true_period)
            })
        
            # Show what periods were actually detected
        detected_periods = [r['best_period'] for r in results if r['detected']]
        if detected_periods:
            print(f"Detected periods: {[f'{p:.2f}' for p in detected_periods]}")

        # Debug: Show what periods were actually found
        found_periods = [r['best_period'] for r in results if r['detected']]
        if len(found_periods) > 0:
            unique_periods = np.unique(np.round(found_periods, 2))
            # Don't print here, return it instead
        
        return results
    

    def run_stress_sweep(self, n_trials=20):
        """
        Run systematic sweep across stress levels
        
        Parameters:
        - n_trials: number of stress levels to test
        
        Returns:
        - sweep_results: comprehensive results across all stress levels
        """
        print("/n" + "=" * 70)
        print("RUNNING SYSTEMATIC STRESS SWEEP")
        print("=" * 70)

        stress_levels = np.linspace(0, 1, n_trials)
        true_period = 5.0

        sweep_results = {
            'stress_levels': [],
            'detection_rates': [],
            'avg_errors': [],
            'avg_powers': [],
            'period_stds': [],
            'detected_periods': []
        }

        for stress in stress_levels:
            results = self.run_single_trial(stress, true_period)

            # Calculate metrics
            n_detected = sum(1 for r in results if r['detected'])
            detection_rate = n_detected / len(results)

            avg_error = np.mean([r['period_error'] for r in results])
            avg_power = np.mean([r['power'] for r in results])

            detected_periods = [r['best_period'] for r in results if r['detected']]
            period_std = np.std(detected_periods) if len(detected_periods) > 1 else 0.0
            avg_detected_period = np.mean(detected_periods) if len(detected_periods) > 0 else 0.0

            # Store results
            sweep_results['stress_levels'].append(stress)
            sweep_results['detection_rates'].append(detection_rate)
            sweep_results['avg_errors'].append(avg_error)
            sweep_results['avg_powers'].append(avg_power)
            sweep_results['period_stds'].append(period_std)
            sweep_results['detected_periods'].append(avg_detected_period)

            # Progress indicator
            if int(stress * 10) % 2 == 0:
                print(f"Progress: {stress:.1f} | Detections: {n_detected}/5 | Error: {avg_error:.3f} | Power: {avg_power:.2f}")

            
        print("=" * 70)
        print("STRESS SWEEP COMPLETE")
        print("=" * 70)

        return sweep_results
    

    def visualize_results(self, sweep_results, true_period=5.0):
        """
        Create comprehensive visualizations of false consensus phenomenon
        """
        stress = np.array(sweep_results['stress_levels'])
        detection_rate = np.array(sweep_results['detection_rates'])
        avg_error = np.array(sweep_results['avg_errors'])
        avg_power = np.array(sweep_results['avg_powers'])
        period_std = np.array(sweep_results['period_stds'])
        detected_periods = np.array(sweep_results['detected_periods'])
        
        # Create comprehensive visualization
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # ========== PANEL 1: Detection Rate vs Stress ==========
        axes[0, 0].plot(stress, detection_rate * 100, 'b-', linewidth=3, marker='o', markersize=6)
        axes[0, 0].axhline(y=100, color='g', linestyle='--', alpha=0.3, label='100% detection')
        axes[0, 0].fill_between(stress, 0, detection_rate * 100, alpha=0.2)
        axes[0, 0].set_xlabel('Environmental Stress Level', fontsize=12)
        axes[0, 0].set_ylabel('Detection Rate (%)', fontsize=12)
        axes[0, 0].set_title('Detection Rate vs. Stress\n(Higher = More Detections)', fontsize=14, fontweight='bold')
        axes[0, 0].grid(True, alpha=0.3)
        axes[0, 0].set_ylim([0, 105])
        axes[0, 0].legend()
        
        # ========== PANEL 2: Period Error vs Stress ==========
        axes[0, 1].plot(stress, avg_error, 'r-', linewidth=3, marker='s', markersize=6)
        axes[0, 1].axhline(y=0.5, color='orange', linestyle='--', alpha=0.5, label='0.5 day error threshold')
        axes[0, 1].fill_between(stress, 0, avg_error, alpha=0.2, color='red')
        axes[0, 1].set_xlabel('Environmental Stress Level', fontsize=12)
        axes[0, 1].set_ylabel('Average Period Error (days)', fontsize=12)
        axes[0, 1].set_title('Detection Accuracy vs. Stress\n(Lower = More Accurate)', fontsize=14, fontweight='bold')
        axes[0, 1].grid(True, alpha=0.3)
        axes[0, 1].legend()
        
        # ========== PANEL 3: Detection Power vs Stress ==========
        axes[1, 0].plot(stress, avg_power, 'g-', linewidth=3, marker='^', markersize=6)
        axes[1, 0].axhline(y=3.0, color='r', linestyle='--', alpha=0.5, label='Detection threshold (3.0)')
        axes[1, 0].fill_between(stress, 0, avg_power, alpha=0.2, color='green')
        axes[1, 0].set_xlabel('Environmental Stress Level', fontsize=12)
        axes[1, 0].set_ylabel('Average Detection Power', fontsize=12)
        axes[1, 0].set_title('Signal Strength vs. Stress\n(Higher = Stronger Signal)', fontsize=14, fontweight='bold')
        axes[1, 0].grid(True, alpha=0.3)
        axes[1, 0].legend()
        
        # ========== PANEL 4: Detected Period vs Stress ==========
        axes[1, 1].plot(stress, detected_periods, 'm-', linewidth=3, marker='d', markersize=6, label='Detected period')
        axes[1, 1].axhline(y=true_period, color='b', linestyle='--', linewidth=2, alpha=0.7, label=f'True period ({true_period} days)')
        axes[1, 1].fill_between(stress, detected_periods - period_std, detected_periods + period_std, 
                                alpha=0.3, color='purple', label='±1 std dev (agreement)')
        axes[1, 1].set_xlabel('Environmental Stress Level', fontsize=12)
        axes[1, 1].set_ylabel('Detected Period (days)', fontsize=12)
        axes[1, 1].set_title('Detected Period vs. Stress\n(Should match blue line)', fontsize=14, fontweight='bold')
        axes[1, 1].grid(True, alpha=0.3)
        axes[1, 1].legend()
        
        plt.tight_layout()
        plt.savefig('false_consensus_comprehensive.png', dpi=150)
        plt.show(block=False)
        plt.pause(0.1)

        # ========== CREATE FALSE CONSENSUS ZONE PLOT ==========
        self._plot_false_consensus_zone(stress, detection_rate, avg_error, avg_power, period_std)

    def _plot_false_consensus_zone(self, stress, detection_rate, avg_error, avg_power, period_std):
        """
        Create the key plot: highlighting the false consensus zone
        """
        # Calculate consensus score (high when detectors agree)
        consensus_score = 1.0 - period_std  # High when std is low
        
        # Calculate false consensus indicator
        # High when: high consensus + high error + high detection rate
        false_consensus = consensus_score * avg_error * detection_rate
        
        fig, axes = plt.subplots(2, 1, figsize=(14, 10))
        
        # ========== TOP: Agreement vs Accuracy ==========
        ax1 = axes[0]
        ax2 = ax1.twinx()
        
        # Plot agreement (left y-axis)
        line1 = ax1.plot(stress, consensus_score, 'b-', linewidth=3, marker='o', 
                         markersize=7, label='Detector Agreement')
        ax1.set_ylabel('Agreement Score\n(1.0 = Perfect Agreement)', fontsize=12, color='b')
        ax1.tick_params(axis='y', labelcolor='b')
        ax1.set_ylim([0, 1.1])
        
        # Plot error (right y-axis)
        line2 = ax2.plot(stress, avg_error, 'r-', linewidth=3, marker='s', 
                         markersize=7, label='Period Error')
        ax2.set_ylabel('Period Error (days)', fontsize=12, color='r')
        ax2.tick_params(axis='y', labelcolor='r')
        
        ax1.set_xlabel('Environmental Stress Level', fontsize=12)
        ax1.set_title('The False Consensus Problem:\nHigh Agreement + High Error = Dangerous!', 
                     fontsize=15, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        
        # Combine legends
        lines = line1 + line2
        labels = [l.get_label() for l in lines]
        ax1.legend(lines, labels, loc='upper left', fontsize=11)
        
        # Highlight false consensus zones (high agreement AND high error)
        false_consensus_mask = (consensus_score > 0.9) & (avg_error > 0.3)
        if np.any(false_consensus_mask):
            for i in range(len(stress)-1):
                if false_consensus_mask[i]:
                    ax1.axvspan(stress[i], stress[i+1], alpha=0.3, color='yellow')
        
        # ========== BOTTOM: False Consensus Score ==========
        axes[1].fill_between(stress, 0, false_consensus, alpha=0.4, color='red', label='False Consensus Risk')
        axes[1].plot(stress, false_consensus, 'r-', linewidth=3, marker='o', markersize=7)
        axes[1].set_xlabel('Environmental Stress Level', fontsize=12)
        axes[1].set_ylabel('False Consensus Score\n(Higher = More Dangerous)', fontsize=12)
        axes[1].set_title('False Consensus Risk Zone\n(Agreement × Error × Detection Rate)', 
                         fontsize=15, fontweight='bold')
        axes[1].grid(True, alpha=0.3)
        
        # Mark the peak danger zone
        max_idx = np.argmax(false_consensus)
        axes[1].plot(stress[max_idx], false_consensus[max_idx], 'r*', markersize=20, 
                    label=f'Peak danger at stress={stress[max_idx]:.2f}')
        axes[1].legend(fontsize=11)
        
        # Shade high-risk zones
        high_risk = false_consensus > 0.5 * np.max(false_consensus)
        for i in range(len(stress)-1):
            if high_risk[i]:
                axes[1].axvspan(stress[i], stress[i+1], alpha=0.2, color='red')
        
        plt.tight_layout()
        plt.savefig('false_consensus_zone.png', dpi=150)
        plt.show()
        
        print("\n" + "=" * 70)
        print("VISUALIZATION COMPLETE")
        print("=" * 70)
        print(f"Peak false consensus at stress level: {stress[max_idx]:.2f}")
        print(f"At this level:")
        print(f"  - Detection rate: {detection_rate[max_idx]*100:.1f}%")
        print(f"  - Average error: {avg_error[max_idx]:.3f} days")
        print(f"  - Average power: {avg_power[max_idx]:.2f}")
        print(f"  - Agreement (consensus): {consensus_score[max_idx]:.3f}")
        print("=" * 70)


if __name__ == "__main__":
    # Initialize experiment
    experiment = FalseConsensusExperiment(n_detectors=5)
    
    # Run comprehensive stress sweep
    sweep_results = experiment.run_stress_sweep(n_trials=20)
    
    # Visualize results
    experiment.visualize_results(sweep_results, true_period=5.0)