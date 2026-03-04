#!/usr/bin/env python3
"""
Simple graphs for science project - no fancy formatting
"""

import numpy as np
import matplotlib.pyplot as plt

print("Generating simple graphs...")

# ============================================================================
# GRAPH 1 FOR SLIDE 4: Simple bar chart
# ============================================================================

fig, ax = plt.subplots(figsize=(10, 6))

detectors = ['Detector 1', 'Detector 2', 'Detector 3', 'Detector 4', 'Detector 5', 'TRUE VALUE']
periods = [7.0, 7.0, 7.0, 7.0, 7.0, 5.0]

bars = ax.bar(detectors, periods, color='steelblue', edgecolor='black', linewidth=2)

# Add period values on bars
for bar, period in zip(bars, periods):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 0.2,
            f'{period} days', ha='center', fontsize=14)

ax.set_ylabel('Period (days)', fontsize=12)
ax.set_title('Detected Periods', fontsize=14)
ax.set_ylim([0, 8])
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('slide4_false_consensus.png', dpi=150)
print("✓ Graph 1 saved: slide4_false_consensus.png")
plt.close()


# ============================================================================
# GRAPH 2 FOR SLIDE 5: Simple 3-panel
# ============================================================================

fig, axes = plt.subplots(3, 1, figsize=(12, 9))

time = np.linspace(0, 35, 840)

# Panel 1: Real Planet
real_planet_flux = np.ones(len(time))
period_real = 5.0
transit_duration = 0.1
transit_depth = 0.02

phase_real = (time % period_real) / period_real
transit_mask = phase_real < (transit_duration / period_real)
real_planet_flux[transit_mask] = 1.0 - transit_depth

axes[0].plot(time, real_planet_flux, 'b-', linewidth=2)
axes[0].set_ylabel('Brightness', fontsize=11)
axes[0].set_title('Real Planet: Transits Every 5 Days', fontsize=13)
axes[0].set_ylim([0.97, 1.02])
axes[0].grid(True, alpha=0.3)

# Panel 2: Temperature
temp_cycle = 0.006 * np.sin(2 * np.pi * time / 7.0)
axes[1].plot(time, temp_cycle, 'r-', linewidth=2)
axes[1].axhline(y=0, color='k', linestyle='--', alpha=0.3)
axes[1].set_ylabel('Temperature Effect', fontsize=11)
axes[1].set_title('Spacecraft Temperature: Every 7 Days', fontsize=13)
axes[1].grid(True, alpha=0.3)
axes[1].text(3.5, 0.005, 'HOT', fontsize=12, ha='center')
axes[1].text(10.5, -0.005, 'COLD', fontsize=12, ha='center')

# Panel 3: Combined
corrupted = real_planet_flux + temp_cycle
axes[2].plot(time, corrupted, 'purple', linewidth=2)
axes[2].set_xlabel('Time (days)', fontsize=11)
axes[2].set_ylabel('What Detectors See', fontsize=11)
axes[2].set_title('Combined Signal', fontsize=13)
axes[2].set_ylim([0.97, 1.02])
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('slide5_why_it_happened.png', dpi=150)
print("✓ Graph 2 saved: slide5_why_it_happened.png")
plt.close()

print("\nDONE! Both graphs saved in current directory")
