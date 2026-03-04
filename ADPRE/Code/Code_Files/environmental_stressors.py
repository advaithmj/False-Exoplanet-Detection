import numpy as np
import matplotlib.pyplot as plt

class EnvironmentalStressors:
    """
    Models deep-space environmental effects that currupt signals
    These affect ALL detectors simultaneously
    """

    @staticmethod
    def thermal_drift(time, drift_rate=0.1, drift_amplitude=0.005):
        """
        Slow baseline shift from thermal variations

        Parameters:
        time : observations times (days)
        drift_rate: how many cycles per observation period
        drift_amplitude: maximum drift
        """

        #temperature cycles (Sinusoidal component)
        sinusoidal = drift_amplitude * np.sin(2 * np.pi * drift_rate * time)

        #gradual warming (Linear trend)
        linear = 0.5 * drift_amplitude * (time / time[-1])

        #Combined drift
        drift = sinusoidal + linear

        return drift

        pass

    @staticmethod
    def radiation_noise(time, intensity=0.01, cluster_size=5):
        """
        Sudden spikes from radiation hits

        Parameters:
        time : observation times (days)
        intensity: average amplitude of radiation spikes
        cluster_size: average number of consecutive points affected
        """

        noise = np.zeros(len(time))

        # Calculate number of radiation events
        n_events = int(len(time) * intensity)

        # Create random radiation hits
        for _ in range(n_events):
            # Random start position for this hit
            start_idx = np.random.randint(0,len(time) - cluster_size)

            # Random spike amplitude
            spike_magnitude = np.random.exponential(0.01)

            # affect a cluster of consecutive points
            noise[start_idx:start_idx + cluster_size] += spike_magnitude

        return noise
        pass

    @staticmethod
    def signal_attenuation(time, flux, attenuation_rate=0.1):
        """
        Gradual signal loss over time (Detector aging)

        Parameters:
        time : observation times (days)
        flux : original signal fluxes
        attenuation_rate: fraction of signal lost per day
        """

        normalized_time = time / time[-1]
        attenuation_factor = np.exp(-attenuation_rate * normalized_time)

        #Multiply flux by attenuation factor
        attenuated_flux = flux * attenuation_factor

        return attenuated_flux

        pass

    @staticmethod
    def timing_jitter(time, jitter_amplitude=0.001):
        """
        Small random shifts in observation times

        Parameters:
        time : observation times (days)
        jitter_amplitude: maximum timing error (days)
        """

        # generate random timing errors 
        jitter = np.random.normal(0, jitter_amplitude, len(time))

        # Add errors to original times
        jittered_time = time + jitter

        # Ensure times remain in order
        # If errors are too large, times could become non-monotonic (not the same length)
        jittered_time = np.sort(jittered_time)

        return jittered_time

        pass



if __name__ == "__main__":
    # Create time array
    time = np.linspace(0, 50, 1200)
    
    print("=" * 70)
    print("ENVIRONMENTAL STRESSORS TEST")
    print("=" * 70)
    
    # ========== TEST 1: THERMAL DRIFT ==========
    print("\nTEST 1: Thermal Drift")
    print("-" * 70)
    
    drift_mild = EnvironmentalStressors.thermal_drift(time, drift_rate=0.1, drift_amplitude=0.003)
    drift_moderate = EnvironmentalStressors.thermal_drift(time, drift_rate=0.2, drift_amplitude=0.006)
    drift_severe = EnvironmentalStressors.thermal_drift(time, drift_rate=0.3, drift_amplitude=0.010)
    
    print(f"Mild drift range: {np.min(drift_mild):.4f} to {np.max(drift_mild):.4f}")
    print(f"Moderate drift range: {np.min(drift_moderate):.4f} to {np.max(drift_moderate):.4f}")
    print(f"Severe drift range: {np.min(drift_severe):.4f} to {np.max(drift_severe):.4f}")
    
    plt.figure(figsize=(14, 6))
    plt.plot(time, drift_mild, 'b-', linewidth=2, label='Mild drift (0.3%)')
    plt.plot(time, drift_moderate, 'orange', linewidth=2, label='Moderate drift (0.6%)')
    plt.plot(time, drift_severe, 'r-', linewidth=2, label='Severe drift (1.0%)')
    plt.axhline(y=0, color='k', linestyle='--', alpha=0.3)
    plt.xlabel('Time (days)', fontsize=12)
    plt.ylabel('Baseline Shift', fontsize=12)
    plt.title('Thermal Drift: Slow Baseline Variations', fontsize=14)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('thermal_drift_test.png', dpi=150)
    plt.show(block=False)
    plt.pause(0.1)
    
    # ========== TEST 2: RADIATION NOISE ==========
    print("\nTEST 2: Radiation Noise")
    print("-" * 70)
    
    # Set random seed for reproducibility
    np.random.seed(42)
    
    rad_mild = EnvironmentalStressors.radiation_noise(time, intensity=0.005, cluster_size=3)
    rad_moderate = EnvironmentalStressors.radiation_noise(time, intensity=0.015, cluster_size=5)
    rad_severe = EnvironmentalStressors.radiation_noise(time, intensity=0.030, cluster_size=8)
    
    print(f"Mild radiation: {np.sum(rad_mild > 0)} affected points")
    print(f"Moderate radiation: {np.sum(rad_moderate > 0)} affected points")
    print(f"Severe radiation: {np.sum(rad_severe > 0)} affected points")
    print(f"Max spike (mild): {np.max(rad_mild):.4f}")
    print(f"Max spike (moderate): {np.max(rad_moderate):.4f}")
    print(f"Max spike (severe): {np.max(rad_severe):.4f}")
    
    fig, axes = plt.subplots(3, 1, figsize=(14, 10))
    
    # Mild radiation
    axes[0].plot(time, rad_mild, 'b-', linewidth=1, alpha=0.7)
    axes[0].set_ylabel('Flux Increase', fontsize=11)
    axes[0].set_title('Mild Radiation (0.5% of time affected)', fontsize=13)
    axes[0].grid(True, alpha=0.3)
    axes[0].set_ylim([-0.001, 0.05])
    
    # Moderate radiation
    axes[1].plot(time, rad_moderate, 'orange', linewidth=1, alpha=0.7)
    axes[1].set_ylabel('Flux Increase', fontsize=11)
    axes[1].set_title('Moderate Radiation (1.5% of time affected)', fontsize=13)
    axes[1].grid(True, alpha=0.3)
    axes[1].set_ylim([-0.001, 0.05])
    
    # Severe radiation
    axes[2].plot(time, rad_severe, 'r-', linewidth=1, alpha=0.7)
    axes[2].set_xlabel('Time (days)', fontsize=12)
    axes[2].set_ylabel('Flux Increase', fontsize=11)
    axes[2].set_title('Severe Radiation (3.0% of time affected)', fontsize=13)
    axes[2].grid(True, alpha=0.3)
    axes[2].set_ylim([-0.001, 0.05])
    
    plt.tight_layout()
    plt.savefig('radiation_noise_test.png', dpi=150)
    plt.show(block=False)
    plt.pause(0.1)
    
    # ========== TEST 3: SIGNAL ATTENUATION ==========
    print("\nTEST 3: Signal Attenuation")
    print("-" * 70)
    
    # Create a constant signal (like a star with constant brightness)
    constant_signal = np.ones(len(time))
    
    # Apply different attenuation rates
    atten_mild = EnvironmentalStressors.signal_attenuation(time, constant_signal, attenuation_rate=0.05)
    atten_moderate = EnvironmentalStressors.signal_attenuation(time, constant_signal, attenuation_rate=0.15)
    atten_severe = EnvironmentalStressors.signal_attenuation(time, constant_signal, attenuation_rate=0.30)
    
    print(f"Mild attenuation: {constant_signal[0]:.4f} → {atten_mild[-1]:.4f} ({(1-atten_mild[-1])*100:.1f}% loss)")
    print(f"Moderate attenuation: {constant_signal[0]:.4f} → {atten_moderate[-1]:.4f} ({(1-atten_moderate[-1])*100:.1f}% loss)")
    print(f"Severe attenuation: {constant_signal[0]:.4f} → {atten_severe[-1]:.4f} ({(1-atten_severe[-1])*100:.1f}% loss)")
    
    plt.figure(figsize=(14, 6))
    plt.plot(time, constant_signal, 'k--', linewidth=2, alpha=0.3, label='Original signal (no degradation)')
    plt.plot(time, atten_mild, 'b-', linewidth=2, label='Mild (5% loss)')
    plt.plot(time, atten_moderate, 'orange', linewidth=2, label='Moderate (15% loss)')
    plt.plot(time, atten_severe, 'r-', linewidth=2, label='Severe (30% loss)')
    plt.xlabel('Time (days)', fontsize=12)
    plt.ylabel('Relative Sensitivity', fontsize=12)
    plt.title('Signal Attenuation: Detector Degradation Over Time', fontsize=14)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.ylim([0.65, 1.05])
    plt.tight_layout()
    plt.savefig('signal_attenuation_test.png', dpi=150)
    plt.show(block=False)
    plt.pause(0.1)

# ========== TEST 4: TIMING JITTER ==========
    print("\nTEST 4: Timing Jitter")
    print("-" * 70)
    
    # Apply different jitter levels
    np.random.seed(42)  # For reproducibility
    jitter_mild = EnvironmentalStressors.timing_jitter(time, jitter_amplitude=0.0005)
    jitter_moderate = EnvironmentalStressors.timing_jitter(time, jitter_amplitude=0.002)
    jitter_severe = EnvironmentalStressors.timing_jitter(time, jitter_amplitude=0.005)
    
    # Calculate actual timing errors
    error_mild = jitter_mild - time
    error_moderate = jitter_moderate - time
    error_severe = jitter_severe - time
    
    print(f"Mild jitter: ±{np.std(error_mild)*24*3600:.1f} seconds (std dev)")
    print(f"Moderate jitter: ±{np.std(error_moderate)*24*3600:.1f} seconds (std dev)")
    print(f"Severe jitter: ±{np.std(error_severe)*24*3600:.1f} seconds (std dev)")
    print(f"Max error (severe): {np.max(np.abs(error_severe))*24*3600:.1f} seconds")
    
    # Plot timing errors over time
    fig, axes = plt.subplots(2, 1, figsize=(14, 10))
    
    # Top: Timing errors
    axes[0].plot(time, error_mild * 24 * 60, 'b.', markersize=2, alpha=0.5, label='Mild')
    axes[0].plot(time, error_moderate * 24 * 60, 'orange', markersize=2, alpha=0.5, label='Moderate')
    axes[0].plot(time, error_severe * 24 * 60, 'r.', markersize=2, alpha=0.5, label='Severe')
    axes[0].axhline(y=0, color='k', linestyle='--', alpha=0.3)
    axes[0].set_ylabel('Timing Error (minutes)', fontsize=11)
    axes[0].set_title('Timing Jitter: Random Timestamp Errors', fontsize=13)
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Bottom: Zoom on small section to see jitter detail
    zoom_start, zoom_end = 10, 12  # 2-day window
    zoom_mask = (time >= zoom_start) & (time <= zoom_end)
    
    axes[1].plot(time[zoom_mask], time[zoom_mask], 'k--', linewidth=2, alpha=0.3, label='Perfect timing')
    axes[1].plot(time[zoom_mask], jitter_severe[zoom_mask], 'r-', linewidth=1, marker='o', 
                markersize=3, label='With severe jitter')
    axes[1].set_xlabel('True Time (days)', fontsize=11)
    axes[1].set_ylabel('Measured Time (days)', fontsize=11)
    axes[1].set_title(f'Zoom: Days {zoom_start}-{zoom_end} (Notice the scatter)', fontsize=13)
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('timing_jitter_test.png', dpi=150)
    plt.show(block=False)
    plt.pause(0.1)

    # ========== TEST 5: COMBINED EFFECTS ==========
    print("\nTEST 5: Combined Thermal Drift + Radiation")
    print("-" * 70)
    
    combined = drift_moderate + rad_moderate
    
    print(f"Combined effect range: {np.min(combined):.4f} to {np.max(combined):.4f}")
    print("Remember: Transit depth is 0.0225 (2.25%)")
    
    plt.figure(figsize=(14, 6))
    plt.plot(time, drift_moderate, 'b-', linewidth=2, alpha=0.5, label='Thermal drift only')
    plt.plot(time, rad_moderate, 'g-', linewidth=1, alpha=0.5, label='Radiation only')
    plt.plot(time, combined, 'r-', linewidth=2, alpha=0.8, label='Combined')
    plt.axhline(y=0, color='k', linestyle='--', alpha=0.3)
    plt.xlabel('Time (days)', fontsize=12)
    plt.ylabel('Total Corruption', fontsize=12)
    plt.title('Combined Environmental Effects', fontsize=14)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('combined_stressors_test.png', dpi=150)
    plt.show()
    
    print("\n" + "=" * 70)
    print("Tests complete! Check the plots.")
    print("=" * 70)
    # Test thermal drift
    time = np.linspace(0, 50, 1200)
    
    # Create different drift levels
    drift_mild = EnvironmentalStressors.thermal_drift(time, drift_rate=0.1, drift_amplitude=0.003)
    drift_moderate = EnvironmentalStressors.thermal_drift(time, drift_rate=0.2, drift_amplitude=0.006)
    drift_severe = EnvironmentalStressors.thermal_drift(time, drift_rate=0.3, drift_amplitude=0.010)
    
    # Visualize
    plt.figure(figsize=(14, 6))
    plt.plot(time, drift_mild, 'b-', linewidth=2, label='Mild drift (0.3%)')
    plt.plot(time, drift_moderate, 'orange', linewidth=2, label='Moderate drift (0.6%)')
    plt.plot(time, drift_severe, 'r-', linewidth=2, label='Severe drift (1.0%)')
    plt.axhline(y=0, color='k', linestyle='--', alpha=0.3)
    plt.xlabel('Time (days)', fontsize=12)
    plt.ylabel('Baseline Shift (fractional flux)', fontsize=12)
    plt.title('Thermal Drift: Slow Baseline Variations', fontsize=14)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('thermal_drift_test.png', dpi=150)
    plt.show()
    
    print("=" * 70)
    print("THERMAL DRIFT TEST")
    print("=" * 70)
    print(f"Mild drift range: {np.min(drift_mild):.4f} to {np.max(drift_mild):.4f}")
    print(f"Moderate drift range: {np.min(drift_moderate):.4f} to {np.max(drift_moderate):.4f}")
    print(f"Severe drift range: {np.min(drift_severe):.4f} to {np.max(drift_severe):.4f}")
    print("\nRemember: Transit depth is only ~0.0225 (2.25%)")
    print("Severe drift can be almost half the transit depth!")

    # ========== TEST 6: ALL STRESSORS ON TRANSIT SIGNAL ==========
    print("\nTEST 6: Complete Corruption - All Stressors on Transit Signal")
    print("-" * 70)
    
    # Generate a clean transit signal (like in detection_algorithms.py)
    period = 5.0
    transit_duration = 0.15
    planet_radius_ratio = 0.15  # Transit depth ~2.25%

    flux_clean = np.ones(len(time))
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
                flux_clean[i] = 1.0 - blocked_area

    np.random.seed(123)
    stellar_noise = np.random.normal(0, 0.002, len(flux_clean))
    flux_with_noise = flux_clean + stellar_noise

    flux_corrupted = flux_with_noise.copy()

    # Apply thermal drift
    drift = EnvironmentalStressors.thermal_drift(time, drift_rate=0.2, drift_amplitude=0.006)
    flux_corrupted += drift

    # Apply radiation noise
    radiation = EnvironmentalStressors.radiation_noise(time, intensity=0.015, cluster_size=5)
    flux_corrupted += radiation

    # Apply signal attenuation
    flux_corrupted = EnvironmentalStressors.signal_attenuation(time, flux_corrupted, attenuation_rate=0.15)

    # Apply timing jitter
    time_jittered = EnvironmentalStressors.timing_jitter(time, jitter_amplitude=0.002)

    print(f"Transit depth (clean): {planet_radius_ratio**2:.4f} ({planet_radius_ratio**2*100:.2f}%)")
    print(f"Stellar noise level: 0.002 (0.2%)")
    print(f"Thermal drift range: {np.min(drift):.4f} to {np.max(drift):.4f}")
    print(f"Radiation events: {np.sum(radiation > 0)} affected points")
    print(f"Signal loss (attenuation): {(1 - flux_corrupted[-1]/flux_clean[-1])*100:.1f}%")
    print(f"Timing jitter: ±{np.std(time_jittered - time)*24*3600:.1f} seconds")

    # Visualize the degration
    fig, axes = plt.subplots(4, 1, figsize=(14, 14))

    # Panel 1: Clean signal
    axes[0].plot(time, flux_clean, 'b-', linewidth=1.5, alpha=0.8)
    axes[0].set_ylabel('Normalized Flux', fontsize=11)
    axes[0].set_title('Level 1: Clean Transit Signal (Ground Truth)', fontsize=13)
    axes[0].grid(True, alpha=0.3)
    axes[0].set_ylim([0.97, 1.03])
    
    # Panel 2: With stellar noise only
    axes[1].plot(time, flux_with_noise, 'g-', linewidth=1, alpha=0.6)
    axes[1].set_ylabel('Normalized Flux', fontsize=11)
    axes[1].set_title('Level 2: + Stellar Noise (Normal Detection Challenge)', fontsize=13)
    axes[1].grid(True, alpha=0.3)
    axes[1].set_ylim([0.97, 1.03])
    
    # Panel 3: With drift and radiation
    flux_partial = flux_with_noise + drift + radiation
    axes[2].plot(time, flux_partial, 'orange', linewidth=1, alpha=0.6)
    axes[2].set_ylabel('Normalized Flux', fontsize=11)
    axes[2].set_title('Level 3: + Thermal Drift + Radiation (Getting Difficult)', fontsize=13)
    axes[2].grid(True, alpha=0.3)
    axes[2].set_ylim([0.97, 1.03])
    
    # Panel 4: Everything (using jittered time) - with auto y-limits
    axes[3].plot(time_jittered, flux_corrupted, 'r-', linewidth=1, alpha=0.6)
    axes[3].set_xlabel('Time (days)', fontsize=12)
    axes[3].set_ylabel('Normalized Flux', fontsize=11)
    axes[3].set_title('Level 4: + Attenuation + Timing Jitter (EXTREME CORRUPTION)', fontsize=13)
    axes[3].grid(True, alpha=0.3)
    # Auto y-limits to show everything
    y_min = np.min(flux_corrupted) - 0.01
    y_max = np.max(flux_corrupted) + 0.01
    axes[3].set_ylim([y_min, y_max])
    
    plt.tight_layout()
    plt.savefig('complete_corruption_test.png', dpi=150)
    plt.show(block=False)
    plt.pause(0.1)
    
    # Create separate detailed plot for Level 4
    print("\nCreating detailed view of fully corrupted signal...")
    
    fig, axes = plt.subplots(2, 1, figsize=(14, 10))
    
    # Top: Full time series with automatic y-limits
    axes[0].plot(time_jittered, flux_corrupted, 'r-', linewidth=1.5, alpha=0.7, label='Fully corrupted')
    axes[0].plot(time, flux_clean, 'b--', linewidth=1, alpha=0.4, label='True signal (hidden)')
    axes[0].set_ylabel('Normalized Flux', fontsize=12)
    axes[0].set_title('Fully Corrupted Signal: All Stressors Combined', fontsize=14)
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Bottom: Zoom on a specific region (days 10-20)
    zoom_start, zoom_end = 10, 20
    zoom_mask = (time >= zoom_start) & (time <= zoom_end)
    zoom_mask_jitter = (time_jittered >= zoom_start) & (time_jittered <= zoom_end)
    
    axes[1].plot(time_jittered[zoom_mask_jitter], flux_corrupted[zoom_mask_jitter], 
                'r-', linewidth=1.5, alpha=0.7, label='Corrupted signal')
    axes[1].plot(time[zoom_mask], flux_clean[zoom_mask], 
                'b--', linewidth=2, alpha=0.6, label='True transits')
    axes[1].set_xlabel('Time (days)', fontsize=12)
    axes[1].set_ylabel('Normalized Flux', fontsize=12)
    axes[1].set_title(f'Zoom: Days {zoom_start}-{zoom_end} (Can you spot the transits?)', fontsize=14)
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('corrupted_signal_detailed.png', dpi=150)
    plt.show()
