# Medical Insurance Project & Actuarial Factor Sensitivity Lab

Welcome to the **Medical Insurance Cost Intelligence Project**, based on Codecademy's *Python Syntax: Medical Insurance Project*.

This repository provides an end-to-end implementation including:
1. **Fully Solved & Executed Jupyter Notebook** with markdown notes, code cells, and terminal outputs.
2. **Core Python Script (`script.py`)** with direct variable manipulation and string concatenation.
3. **Modular Python Engine (`insurance_calculator.py`)** with reusable functions and CLI reporting.
4. **Interactive Web Application (`index.html` & `server.js`)** featuring real-time sliders, mathematical waterfall breakdowns, sensitivity analysis, and code walkthroughs.

---

## 🧮 The Insurance Cost Formula

The actuarial regression formula used in this project estimates yearly individual health insurance costs in dollars:

$$\text{insurance\_cost} = 250 \times \text{age} - 128 \times \text{sex} + 370 \times \text{bmi} + 425 \times \text{num\_of\_children} + 24,000 \times \text{smoker} - 12,500$$

### Variables Dictionary

| Variable | Type | Description | Baseline Value |
| :--- | :--- | :--- | :--- |
| `age` | `int` | Age of the individual in years | `28` |
| `sex` | `int` | Biological sex: `0` for female, `1` for male | `0` (Female) |
| `bmi` | `float` | Body Mass Index ($kg/m^2$) | `26.2` |
| `num_of_children` | `int` | Number of dependent children | `3` |
| `smoker` | `int` | Smoking status: `0` for non-smoker, `1` for smoker | `0` (Non-smoker) |

---

## 📊 Summary of Factor Findings

| Factor Experiment | Code Change | New Cost | Delta vs Baseline | Key Insight |
| :--- | :--- | :--- | :--- | :--- |
| **Baseline Profile** | Initial values | **$5,469.00** | $0.00 | 28yo non-smoking woman with 3 children |
| **Age Factor** | `age += 4` | **$6,469.00** | **+$1,000.00** | Linear increase of +$250/year of age |
| **BMI Factor** | `bmi += 3.1` | **$6,616.00** | **+$1,147.00** | Linear increase of +$370 per BMI point |
| **Biological Sex** | `sex = 1` | **$5,341.00** | **-$128.00** | Men had slightly lower average costs (-$128) |
| **Smoker Factor** | `smoker = 1` | **$29,469.00** | **+$24,000.00** | Overwhelming risk driver (+438.8% increase) |
| **Dependent Children** | `children += 1` | **$5,894.00** | **+$425.00** | Marginal increase of +$425 per child |

---

## 📁 Project Directory Structure

```text
medical_insurance/
├── Python Syntax Medical Insurance Project.ipynb           # Solved & fully executed notebook
├── Python Syntax Medical Insurance Project_Solution.ipynb  # Codecademy reference solution
├── script.py                                               # Official Codecademy solution script
├── insurance_calculator.py                                 # Modular Python module & CLI
├── index.html                                              # Interactive Web Application
├── server.js                                               # Local dev server with live API
├── package.json                                            # Node.js project configuration
└── README.md                                               # Documentation
```

---

## 🚀 How to Run

### 1. Run Python Script
```bash
python script.py
```

### 2. Run Modular Calculator CLI
```bash
python insurance_calculator.py
```

### 3. Launch Interactive Web App
You can double-click `index.html` to open it in any browser, or run the local Node server:
```bash
node server.js
```
Then open `http://localhost:3000` in your web browser.

---

## 💡 Data Science Reflections
- **BMI Caution:** While insurance underwriters frequently utilize BMI, BMI does not distinguish between lean muscle mass and adipose tissue. As data practitioners, we should remain mindful of single-metric health proxies.
- **Actuarial Risk Pricing:** Smoking adds an immense $24,000 annual surcharge in this model, accurately highlighting the disproportionate clinical risks associated with cardiovascular and pulmonary diseases.
