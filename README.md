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
├── medicare_dictionary.py                                  # Complete Medicare glossary, metrics, scripts & forms
├── medicare_assistant.py                                   # Interactive Medicare Command Center CLI
├── medicare_dictionary.json                                # Machine-readable Medicare database
├── index.html                                              # Interactive Web Application
├── server.js                                               # Local dev server with live API
├── package.json                                            # Node.js project configuration
└── README.md                                               # Documentation
```

---

## 🏥 Medicare Command Center & Dictionary CLI

Launch the interactive Medicare field assistant or execute direct commands:

```bash
# Interactive REPL mode:
python medicare_assistant.py

# Direct CLI execution examples:
python medicare_assistant.py magic                   # View the 5 essential field metrics
python medicare_assistant.py dict IRMAA              # Look up any term definition
python medicare_assistant.py calc-ppsp 1850          # Calculate monthly EFT bank draft
python medicare_assistant.py calc-part-a 75          # Calculate hospital stay out-of-pocket
python medicare_assistant.py calc-snf 45             # Calculate SNF rehab liability
python medicare_assistant.py calc-part-b 4000        # Calculate Part B deductible + coinsurance
python medicare_assistant.py calc-irmaa 145000 single # Calculate IRMAA Part B & D surcharge
python medicare_assistant.py calc-penalty-d 36       # Calculate lifelong Part D penalty
python medicare_assistant.py plan G                  # Inspect Medigap Plan G coverage
python medicare_assistant.py script socialsecurity   # View Bankers Life Social Security close
python medicare_assistant.py checkpoint 5            # View Bankers Life checkpoint Q&A #5
```

### Allowed Commands Reference

| Command | Usage | Description |
| :--- | :--- | :--- |
| `help [command]` | `help calc-part-a` | View syntax & examples for all allowed commands |
| `dict <term>` | `dict IRMAA` | Query definition from official CMS handbook & Bankers Life guide |
| `terms` | `terms` | List all indexed dictionary terms categorized |
| `magic` | `magic` | Display the 5 'Magic Numbers' & essential field training metrics |
| `calc-part-a <days>` | `calc-part-a 65` | Inpatient hospital deductible, daily coinsurance & reserve days |
| `calc-snf <days>` | `calc-snf 40` | Skilled Nursing Facility rehab coinsurance (Days 21-100: $217/day) |
| `calc-part-b <bills>` | `calc-part-b 2500` | Part B $283 annual deductible + 20% patient coinsurance |
| `calc-ppsp <annual>` | `calc-ppsp 1850` | Bankers Life PPSP formula: `(annual * 0.08583) + $1.00` |
| `calc-irmaa <income> <status>` | `calc-irmaa 150000 single` | 2026 IRMAA surcharge tiers for Parts B and D |
| `calc-penalty-d <months>` | `calc-penalty-d 24` | Lifelong 1%/mo Part D late enrollment penalty |
| `calc-total ...` | `calc-total 10 30 4000 85000 single` | Full multi-part annual medical out-of-pocket simulation |
| `script <name>` | `script turning65` | Bankers Life sales scripts (turning65, working65, under65, socialsecurity, assumptive, trial) |
| `plan <letter>` | `plan G` | Standardized Medigap coverage matrix (Plans A-N) |
| `periods [code]` | `periods IEP` | Enrollment windows (IEP, AEP, MA_OEP, GEP, SEP, Medigap_OEP) |
| `checkpoint <1-18>` | `checkpoint all` | Bankers Life Participant's Guide Checkpoint answer key |
| `quiz` | `quiz` | Interactive 5-question agent certification quiz |
| `export-json` | `export-json` | Export entire Medicare dictionary to JSON |
| `exit` | `exit` | Quit the application |

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

### 3. Run Medicare Command Center
```bash
python medicare_assistant.py
```

### 4. Launch Interactive Web App
You can double-click `index.html` to open it in any browser, or run the local Node server:
```bash
node server.js
```
Then open `http://localhost:3000` in your web browser.

---

## 💡 Data Science & Actuarial Reflections
- **BMI Caution:** While insurance underwriters frequently utilize BMI, BMI does not distinguish between lean muscle mass and adipose tissue. As data practitioners, we should remain mindful of single-metric health proxies.
- **Actuarial Risk Pricing:** Smoking adds an immense $24,000 annual surcharge in this model, accurately highlighting the disproportionate clinical risks associated with cardiovascular and pulmonary diseases.
- **Medigap Plan G Protection:** Eliminates the uncapped 20% Part B coinsurance and $1,736 Part A hospital deductible, leaving the beneficiary with only the $283 annual Part B deductible as their sole out-of-pocket medical liability.

