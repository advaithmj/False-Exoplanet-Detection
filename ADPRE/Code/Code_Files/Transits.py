from cmath import phase
import numpy as np
import matplotlib.pyplot as plt

def simple_constant_star():
    print("=" * 70)
    print("Constant brightness star simulation")
    print("=" * 70)

    time = np.linspace(0, 10, 240)
    flux = np.ones(len(time))

    plt.figure(figsize=(12, 4))
    plt.plot(time, flux, 'b-', linewidth=2)
    plt.xlabel("Time (days)", fontsize=12)
    plt.ylabel("Normalized Flux", fontsize=12)
    plt.title('Baseline: Constant Brightness Star', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.ylim(0.95, 1.05)
    plt.axhline(1.0, color='k', linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.savefig("constant_star.png", dpi=150)
    plt.show(block=False)
    plt.pause(0.1)

def single_transit_event():
    print("=" * 70)
    print("Single transit event simulation")
    print("=" * 70)

    time = np.linspace(0, 10, 240)
    flux = np.ones(len(time))

    
    transit_start = 4.0
    transit_duration = 0.2
    transit_detpth = 0.02

    # Realistic transit with gradual ingress/egress
    planet_radius_ratio = 0.1  # Jupiter-like planet

    for i, t in enumerate(time):
        # Calculate time relative to transit center
        time_from_center = abs(t - (transit_start + transit_duration/2))
        
        if time_from_center < transit_duration/2:
            # Normalized position: 0 = center, 1 = edge
            normalized_pos = time_from_center / (transit_duration/2)
            
            if normalized_pos < (1 - planet_radius_ratio):
                # Planet fully on disk
                blocked_area = planet_radius_ratio**2
            else:
                # Planet at edge - partial overlap
                overlap_fraction = (1 - normalized_pos) / planet_radius_ratio
                overlap_fraction = max(0, min(1, overlap_fraction))
                blocked_area = planet_radius_ratio**2 * overlap_fraction
            
            flux[i] = 1.0 - blocked_area

    plt.figure(figsize=(12, 4))
    plt.plot(time, flux, 'b-', linewidth=2)
    plt.axvline(x=transit_start, color='r', linestyle='--', alpha=0.5, label='Transit starts')
    plt.axvline(x=transit_start + transit_duration, color='r', linestyle='--', alpha=0.5, label='Transit ends')
    plt.xlabel('Time (days)', fontsize=12)
    plt.ylabel('Normalized Flux', fontsize=12)
    plt.title('Single Transit: Planet Blocks 2% of Starlight', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.ylim([0.95, 1.05])
    plt.legend()
    plt.tight_layout()
    plt.savefig('Single_Transit.png', dpi=150)
    plt.show(block=False)
    plt.pause(0.1)

def periodic_transits():
    print("=" * 70)
    print("Periodic transit events simulation")
    print("=" * 70)

    time = np.linspace(0, 30, 720)
    flux = np.ones(len(time))

    orbital_period = 5.0
    transit_duration = 0.15
    transit_depth = 0.015

    # Instead of simple box, calculate gradual ingress/egress
    transit_fraction = transit_duration / orbital_period
    planet_radius_ratio = 0.1  # Planet radius / Star radius (Jupiter-like)

    phase = (time % orbital_period) / orbital_period
    # Loop through each time point
    for i, p in enumerate(phase):
        if p < transit_fraction:
            # Calculate how far across the star the planet is
            # normalized_pos: 0 = center of transit, 1 = edge
            normalized_pos = abs(2 * p / transit_fraction - 1)
            
            if normalized_pos < 1:
                # Planet is on the star's disk
                if normalized_pos < (1 - planet_radius_ratio):
                    # Planet fully on disk - maximum blocking
                    blocked_area = planet_radius_ratio**2
                else:
                    # Planet partially on disk (ingress or egress)
                    # Linear approximation of overlap
                    overlap_fraction = (1 - normalized_pos) / planet_radius_ratio
                    overlap_fraction = max(0, min(1, overlap_fraction))
                    blocked_area = planet_radius_ratio**2 * overlap_fraction
                
                flux[i] = 1.0 - blocked_area

    plt.figure(figsize=(14, 5))
    plt.plot(time, flux, 'b-', linewidth=2)
    plt.xlabel('Time (days)', fontsize=12)
    plt.ylabel('Normalized Flux', fontsize=12)
    plt.title(f'Periodic Transits: Planet with {orbital_period}-day Orbit', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.ylim([0.97, 1.02])
    plt.pause(0.1)

    transit_times = np.arange(0, 30, orbital_period)
    for t in transit_times:
        plt.axvline(x=t, color='r', linestyle='--', alpha=0.3)

    plt.tight_layout()
    plt.savefig('Periodic_Transits.png', dpi=150)
    plt.show(block=False)

    return time, flux, orbital_period

def add_stellar_noise(time, flux, noise_level=0.002):
    print("=" * 70)
    print("Adding stellar variability noise")
    print("=" * 70)

    noise = np.random.normal(0, noise_level, size=len(flux))
    flux_noisy = flux + noise

    fig, axes = plt.subplots(2, 1, figsize=(14, 8))

    axes[0].plot(time, flux, 'b-', linewidth=2, label='Perfect signal (no noise)')
    axes[0].set_ylabel('Normalized Flux', fontsize=12)
    axes[0].set_title('Clean Signal - What We Wish We Could See', fontsize=14)
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()
    axes[0].set_ylim([0.97, 1.02])
    
    # Bottom plot: noisy signal
    axes[1].plot(time, flux_noisy, 'r-', linewidth=1, alpha=0.7, label='With stellar noise')
    axes[1].set_xlabel('Time (days)', fontsize=12)
    axes[1].set_ylabel('Normalized Flux', fontsize=12)
    axes[1].set_title('Noisy Signal - What We Actually Observe', fontsize=14)
    axes[1].grid(True, alpha=0.3)
    axes[1].legend()
    axes[1].set_ylim([0.97, 1.02])

    plt.tight_layout()
    plt.savefig('Stellar_Noise_Comparison.png', dpi=150)
    plt.show(block=False)
    plt.pause(0.1)

    return flux_noisy

def demonstrate_phase_folding(time, flux_noisy, period):
    print("=" * 70)
    print("Demonstrating phase folding")
    print("=" * 70)

    phase = (time % period) / period

    # Sort by phase
    sorted_indices = np.argsort(phase)
    phase_sorted = phase[sorted_indices]
    flux_sorted = flux_noisy[sorted_indices]

    fig, axes = plt.subplots(2, 1, figsize=(14, 8))

    # Top: time series (what we actually observe)
    axes[0].plot(time, flux_noisy, 'b-', linewidth=1, alpha=0.6)
    axes[0].set_xlabel('Time (days)', fontsize=12)
    axes[0].set_ylabel('Normalized Flux', fontsize=12)
    axes[0].set_title('Time Series: Hard to See Individual Transits in Noise', fontsize=14)
    axes[0].grid(True, alpha=0.3)
    
    # Bottom: phase-folded (all transits aligned)
    axes[1].plot(phase_sorted, flux_sorted, 'r.', markersize=3, alpha=0.5)
    axes[1].set_xlabel('Orbital Phase (0 = transit center)', fontsize=12)
    axes[1].set_ylabel('Normalized Flux', fontsize=12)
    axes[1].set_title('Phase-Folded: All Transits Stacked - Signal Becomes Clear!', fontsize=14)
    axes[1].grid(True, alpha=0.3)
    axes[1].set_xlim([0, 1])

    plt.tight_layout()
    plt.savefig('Phase_Folding_Demonstration.png', dpi=150)
    plt.show(block=False)
    plt.pause(0.1)

if __name__ == "__main__":
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║  EXOPLANET DETECTION ")
    print("╚" + "=" * 68 + "╝")
    print("\n")
    
    # Part 1: Constant star
    simple_constant_star()
    input("Press Enter to continue to Part 2...")
    
    # Part 2: Single transit
    single_transit_event()
    input("Press Enter to continue to Part 3...")
    
    # Part 3: Periodic transits
    time, flux_clean, period = periodic_transits()
    input("Press Enter to continue to Part 4...")
    
    # Part 4: Add noise
    flux_noisy = add_stellar_noise(time, flux_clean)
    input("Press Enter to continue to Part 5...")
    
    # Part 5: Phase folding
    demonstrate_phase_folding(time, flux_noisy, period)
    
    print("\n" + "=" * 70)