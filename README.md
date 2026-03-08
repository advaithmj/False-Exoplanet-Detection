# False Exoplanet Detection

**Multiple independent detectors can achieve perfect consensus while being completely wrong.**

---

## The Problem

Transit-based exoplanet detection relies on identifying small dips in stellar brightness.  
However, stellar variability, instrumental noise, and eclipsing binaries can produce signals that look nearly identical to true planetary transits.  
When multiple models agree on these signals, they can create high-confidence false positives that distort scientific conclusions.

---

## Key Findings

- **1. Model agreement does not guarantee correctness.** Independent classifiers can converge on the same incorrect signal when trained on similar feature distributions.  
- **2. Noise stability metrics outperform raw transit depth.** Variance-based features were stronger predictors than depth alone.  
- **3. Feature engineering matters more than model complexity.** Ensemble methods with engineered inputs outperformed deeper neural networks.  
- **4. False positives exhibit measurable asymmetry.** Skewness and flux instability consistently differentiated non-planetary signals.  
- **5. Precision improves significantly with signal validation layers.** Adding stability scoring reduced false positive rates without major recall loss.  

---

## How to Run

**Clone the repository:**

git clone https://github.com/yourusername/False-Exoplanet-Detection.git
cd False-Exoplanet-Detection

**Create virtual environment (recommended):**

python3 -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

**Install dependencies:**

pip install -r requirements.txt

**Run preprocessing and training:**

python src/preprocessing.py
python src/train.py
python src/evaluate.py

---

**Citation**

Citation details will be added upon ArXiv publication.

---

**License**

This project is licensed under the MIT License.

Published: Zenodo — DOI: 10.5281/zenodo.18912771

