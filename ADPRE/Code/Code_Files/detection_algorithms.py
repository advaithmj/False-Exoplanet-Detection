import numpy as np
import matplotlib.pyplot as plt

class BoxLeastSquaresDetector:
    def __init__(self, period_min=0.5, period_max=20.0, n_periods=100):
        # Initialize the detector
        self.period_min = period_min  # Shortest period to search (days)
        self.period_max = period_max  # Longest period to search (days)
        self.periods = np.linspace(period_min, period_max, n_periods)


    def fold_at_period(self, time, flux, period):
        """Fold the light curve at a specific period"""
        # Calculate phase for each observation
        phase = (time % period) / period
        
        # Sort by phase
        sorted_indices = np.argsort(phase)
        phase_sorted = phase[sorted_indices]
        flux_sorted = flux[sorted_indices]

        return phase_sorted, flux_sorted
    

    def calculate_transit_power(self, phase, flux):
        """
        Calculate how well a box-shaped transit fits this folded light curve
        Uses chi-squared approach to fit a box model to the data
        """
        n_points = len(flux)
        
        if n_points < 10:
            return 0.0
        
        # Try different transit widths (5% to 30% of orbit)
        best_chi2 = 0.0
        
        for transit_width in [0.05, 0.10, 0.15, 0.20, 0.25, 0.30]:
            # Try different transit positions
            for transit_center in np.linspace(0, 1, 20):
                # Define which points are "in transit"
                # Handle wrap-around at phase=1
                if transit_center - transit_width/2 < 0:
                    in_transit = ((phase >= (transit_center - transit_width/2 + 1)) | 
                                 (phase <= (transit_center + transit_width/2)))
                elif transit_center + transit_width/2 > 1:
                    in_transit = ((phase >= (transit_center - transit_width/2)) | 
                                 (phase <= (transit_center + transit_width/2 - 1)))
                else:
                    in_transit = ((phase >= (transit_center - transit_width/2)) & 
                                 (phase <= (transit_center + transit_width/2)))
                
                n_in = np.sum(in_transit)
                n_out = n_points - n_in
                
                if n_in < 3 or n_out < 3:
                    continue
                
                # Calculate in-transit and out-of-transit means
                flux_in = np.mean(flux[in_transit])
                flux_out = np.mean(flux[~in_transit])
                
                # Calculate standard deviation
                std_in = np.std(flux[in_transit])
                std_out = np.std(flux[~in_transit])
                std_all = np.sqrt((std_in**2 * n_in + std_out**2 * n_out) / n_points)
                
                if std_all == 0:
                    continue
                
                # Chi-squared: how different are in-transit vs out-of-transit?
                depth = flux_out - flux_in
                
                if depth > 0:  # Only consider dips, not bumps
                    # Signal-to-noise of the depth measurement
                    chi2 = (depth / std_all) * np.sqrt(n_in * n_out / n_points)
                    
                    if chi2 > best_chi2:
                        best_chi2 = chi2
        
        return best_chi2


    def detect(self, time, flux, threshold=3.0):
        """
        Search for transits across all possible periods
        Returns detected (bool) and results (dict)
        """
        powers = []

        # Try each period
        for period in self.periods:
            # Fold data at this period
            phase, flux_folded = self.fold_at_period(time, flux, period)

            # Calculate how good this period is
            power = self.calculate_transit_power(phase, flux_folded)
            powers.append(power)

        powers = np.array(powers)
        
        # Find the best period
        best_idx = np.argmax(powers)
        best_period = self.periods[best_idx]
        best_power = powers[best_idx]

        # Is it good enough to call a detection?
        detected = best_power > threshold

        results = {
            'detected': detected,
            'best_period': best_period,
            'power': best_power,
            'confidence': min(best_power / threshold, 1.0) if detected else 0.0,
            'all_periods': self.periods,
            'all_powers': powers
        }

        return detected, results


if __name__ == "__main__":
    # Generate test data
    time = np.linspace(0, 50, 1200)
    flux = np.ones(len(time))
    
    # Add a planet signal
    period = 5.0
    transit_duration = 0.15
    planet_radius_ratio = 0.15
    
    phase = (time % period) / period
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
    
    # Add noise
    noise = np.random.normal(0, 0.002, len(flux))
    flux_noisy = flux + noise
    
    # Diagnostics
    print("=" * 70)
    print("SIGNAL CHARACTERISTICS")
    print("=" * 70)
    print(f"Observation duration: {time[-1]:.1f} days")
    print(f"Number of transits: {int(time[-1] / period)}")
    print(f"Transit depth: {planet_radius_ratio**2:.4f} ({planet_radius_ratio**2 * 100:.2f}%)")
    print(f"Noise level: 0.002 (0.2%)")
    print(f"Signal-to-Noise Ratio: {(planet_radius_ratio**2) / 0.002:.2f}")
    
    # Visualization
    fig, axes = plt.subplots(3, 1, figsize=(14, 11))

    # Panel 1: Pure noise
    axes[0].plot(time, flux_noisy - flux, 'gray', linewidth=1, alpha=0.7, label='Noise only')
    axes[0].axhline(y=0, color='k', linestyle='--', linewidth=1, alpha=0.5)
    axes[0].set_ylabel('Noise Level', fontsize=11)
    axes[0].set_title('Pure Noise Component', fontsize=13)
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # Panel 2: Observed data
    axes[1].plot(time, flux_noisy, 'b.', markersize=2, alpha=0.5, label='Observed data')
    axes[1].plot(time, flux, 'r-', linewidth=2, alpha=0.7, label='True signal')
    axes[1].set_ylabel('Normalized Flux', fontsize=11)
    axes[1].set_title('Time Series: Signal + Noise', fontsize=13)
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    # Panel 3: Phase-folded
    phase_true = (time % period) / period
    sort_idx = np.argsort(phase_true)
    axes[2].plot(phase_true[sort_idx], flux_noisy[sort_idx], 'b.', markersize=3, alpha=0.5, label='Folded data')
    axes[2].plot(phase_true[sort_idx], flux[sort_idx], 'r-', linewidth=2, alpha=0.7, label='True signal')
    axes[2].set_xlabel('Orbital Phase', fontsize=11)
    axes[2].set_ylabel('Normalized Flux', fontsize=11)
    axes[2].set_title(f'Phase-Folded at {period} days', fontsize=13)
    axes[2].legend()
    axes[2].grid(True, alpha=0.3)
    axes[2].set_xlim([0, 1])

    plt.tight_layout()
    plt.savefig('signal_visualization.png', dpi=150)
    plt.show(block=False)
    plt.pause(0.1)
    
    # Detection test
    print("\n" + "=" * 70)
    print("DETECTION RESULTS")
    print("=" * 70)
    
    detector = BoxLeastSquaresDetector(period_min=3.0, period_max=7.0, n_periods=400)
    detected, results = detector.detect(time, flux_noisy, threshold=0.5)
    
    print(f"\nDetected: {detected}")
    print(f"Best period: {results['best_period']:.2f} days (true: {period:.2f})")
    print(f"Power: {results['power']:.2f}")
    print(f"Confidence: {results['confidence']:.1%}")
    print("=" * 70)
    
    # Periodogram plot
    plt.figure(figsize=(12, 5))
    plt.plot(results['all_periods'], results['all_powers'], 'b-', linewidth=2)
    plt.axvline(x=period, color='r', linestyle='--', label=f'True period ({period} days)')
    plt.axhline(y=0.5, color='g', linestyle='--', alpha=0.5, label='Detection threshold')
    plt.xlabel('Period (days)', fontsize=12)
    plt.ylabel('Detection Power', fontsize=12)
    plt.title('BLS Periodogram', fontsize=14)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('bls_periodogram.png', dpi=150)
    plt.show()