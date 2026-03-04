import numpy as np
import matplotlib.pyplot as plt

print("Generating graphs for your presentation...")

# ============================================================================
# GRAPH 1 FOR SLIDE 4: All Detectors Found Wrong Period
# ============================================================================

fig, ax = plt.subplots(figsize=(12, 7))

detectors = ['Detector 1', 'Detector 2', 'Detector 3', 'Detector 4', 'Detector 5', 'TRUE\nVALUE']
periods = [7.0, 7.0, 7.0, 7.0, 7.0, 5.0]
colors = ['#ff6b6b', '#ff6b6b', '#ff6b6b', '#ff6b6b', '#ff6b6b', '#4ecdc4']

bars = ax.bar(detectors, periods, color=colors, edgecolor='black', linewidth=3, width=0.6)

# Add value labels on bars
for i, (bar, period) in enumerate(zip(bars, periods)):
    height = bar.get_height()
    if i < 5:
        label = f'{period} days\n❌ WRONG'
        text_color = 'darkred'
    else:
        label = f'{period} days\n✓ CORRECT'
        text_color = 'darkgreen'
    ax.text(bar.get_x() + bar.get_width()/2., height + 0.3,
            label, ha='center', va='bottom', fontsize=16, fontweight='bold',
            color=text_color)

# Add perfect agreement annotation
ax.annotate('PERFECT AGREEMENT\n(All detected 7.0 days)', 
            xy=(2, 7.5), fontsize=18, ha='center',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7),
            fontweight='bold')

ax.set_ylabel('Detected Period (days)', fontsize=16, fontweight='bold')
ax.set_title('FALSE CONSENSUS: All 5 Detectors Agreed on Wrong Answer', 
             fontsize=18, fontweight='bold', pad=20)
ax.set_ylim([0, 9])
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.axhline(y=5.0, color='green', linestyle='--', linewidth=2, alpha=0.5, label='True Period')

# Add legend
ax.legend(fontsize=14, loc='upper right')

plt.tight_layout()
plt.savefig('/Users/advaithjohn/Desktop/ADPRE/Project/slide4_false_consensus.png', dpi=150, bbox_inches='tight')
print("✓ Graph 1 saved: slide4_false_consensus.png")
plt.close()


# ============================================================================
# GRAPH 2 FOR SLIDE 5: Why It Happened (Temperature Cycling)
# ============================================================================

fig, axes = plt.subplots(3, 1, figsize=(14, 10))

# Simulation time
time = np.linspace(0, 35, 840)  # 35 days

# Panel 1: Real Planet Signal (5-day period)
real_planet_flux = np.ones(len(time))
period_real = 5.0
transit_duration = 0.1
transit_depth = 0.02

phase_real = (time % period_real) / period_real
transit_mask = phase_real < (transit_duration / period_real)
real_planet_flux[transit_mask] = 1.0 - transit_depth

axes[0].plot(time, real_planet_flux, 'b-', linewidth=2)
axes[0].set_ylabel('Brightness', fontsize=13, fontweight='bold')
axes[0].set_title('REAL PLANET: Transits Every 5 Days', fontsize=15, fontweight='bold')
axes[0].set_ylim([0.97, 1.02])
axes[0].grid(True, alpha=0.3)

# Panel 2: Spacecraft Temperature (7-day cycle)
temp_cycle = 0.006 * np.sin(2 * np.pi * time / 7.0)
axes[1].plot(time, temp_cycle, 'r-', linewidth=3)
axes[1].axhline(y=0, color='k', linestyle='--', alpha=0.3)
axes[1].set_ylabel('Temperature\nEffect', fontsize=13, fontweight='bold')
axes[1].set_title('SPACECRAFT TEMPERATURE: Heats Up & Cools Down Every 7 Days', 
                  fontsize=15, fontweight='bold', color='red')
axes[1].grid(True, alpha=0.3)
axes[1].annotate('HOT', xy=(3.5, 0.005), fontsize=14, ha='center', color='red', fontweight='bold')
axes[1].annotate('COLD', xy=(7, -0.005), fontsize=14, ha='center', color='blue', fontweight='bold')
axes[1].annotate('HOT', xy=(10.5, 0.005), fontsize=14, ha='center', color='red', fontweight='bold')

# Panel 3: What Detectors Actually See (combined)
corrupted = real_planet_flux + temp_cycle
axes[2].plot(time, corrupted, 'purple', linewidth=2, alpha=0.8)
axes[2].plot(time, real_planet_flux, 'b--', linewidth=1, alpha=0.4, label='Real planet (hidden)')
axes[2].set_xlabel('Time (days)', fontsize=13, fontweight='bold')
axes[2].set_ylabel('What Detectors\nActually See', fontsize=13, fontweight='bold')
axes[2].set_title('WHAT DETECTORS SEE: Temperature Pattern DOMINATES', 
                  fontsize=15, fontweight='bold', color='purple')
axes[2].set_ylim([0.97, 1.02])
axes[2].grid(True, alpha=0.3)
axes[2].legend(fontsize=12)

# Add big explanation
fig.text(0.5, 0.02, 'All detectors see the 7-day temperature pattern (Panel 2) and think it\'s a planet!', 
         ha='center', fontsize=16, fontweight='bold', 
         bbox=dict(boxstyle='round,pad=0.8', facecolor='yellow', alpha=0.8))

plt.tight_layout(rect=[0, 0.04, 1, 1])
plt.savefig('/Users/advaithjohn/Desktop/ADPRE/Project/slide5_why_it_happened.png', dpi=150, bbox_inches='tight')
print("✓ Graph 2 saved: slide5_why_it_happened.png")
plt.close()


print("\n" + "="*70)
print("DONE! Both graphs created:")
print("  1. slide4_false_consensus.png    → Use for SLIDE 4")
print("  2. slide5_why_it_happened.png    → Use for SLIDE 5")
print("="*70)
print("\nBoth saved in: /Users/advaithjohn/Desktop/ADPRE/Project/")
