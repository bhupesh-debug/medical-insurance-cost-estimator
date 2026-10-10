"""
Medical Insurance Cost Intelligence & Factor Sensitivity Module
Based on Codecademy's Python Syntax: Medical Insurance Project.
"""

from typing import Dict, Any

def calculate_insurance_cost(
    age: float,
    sex: int,
    bmi: float,
    num_of_children: int,
    smoker: int
) -> float:
    """
    Calculate estimated yearly medical insurance cost based on actuarial formula:
    insurance_cost = 250*age - 128*sex + 370*bmi + 425*num_of_children + 24000*smoker - 12500

    Parameters:
        age (float): Age of the individual in years
        sex (int): 0 for female, 1 for male
        bmi (float): Body mass index
        num_of_children (int): Number of dependent children
        smoker (int): 0 for non-smoker, 1 for smoker

    Returns:
        float: Estimated yearly insurance cost in dollars
    """
    return (
        250 * age
        - 128 * sex
        + 370 * bmi
        + 425 * num_of_children
        + 24000 * smoker
        - 12500
    )


def run_factor_analysis() -> Dict[str, Any]:
    """
    Execute sensitivity analysis on demographic factors as defined in Tasks 1-13.
    """
    # Task 1: Baseline variables
    baseline_age = 28
    baseline_sex = 0
    baseline_bmi = 26.2
    baseline_children = 3
    baseline_smoker = 0

    # Task 2 & 3: Baseline calculation
    baseline_cost = calculate_insurance_cost(
        baseline_age, baseline_sex, baseline_bmi, baseline_children, baseline_smoker
    )

    # Task 4-7: Age factor (+4 years)
    age_cost = calculate_insurance_cost(
        baseline_age + 4, baseline_sex, baseline_bmi, baseline_children, baseline_smoker
    )
    age_delta = age_cost - baseline_cost

    # Task 8-9: BMI factor (+3.1 BMI)
    bmi_cost = calculate_insurance_cost(
        baseline_age, baseline_sex, baseline_bmi + 3.1, baseline_children, baseline_smoker
    )
    bmi_delta = bmi_cost - baseline_cost

    # Task 10-12: Sex factor (female 0 -> male 1)
    sex_cost = calculate_insurance_cost(
        baseline_age, 1, baseline_bmi, baseline_children, baseline_smoker
    )
    sex_delta = sex_cost - baseline_cost

    # Task 13: Extra Practice - Smoker factor
    smoker_cost = calculate_insurance_cost(
        baseline_age, baseline_sex, baseline_bmi, baseline_children, 1
    )
    smoker_delta = smoker_cost - baseline_cost

    # Task 13: Extra Practice - Additional Child (+1)
    child_cost = calculate_insurance_cost(
        baseline_age, baseline_sex, baseline_bmi, baseline_children + 1, baseline_smoker
    )
    child_delta = child_cost - baseline_cost

    return {
        "baseline_cost": baseline_cost,
        "age_delta": age_delta,
        "bmi_delta": bmi_delta,
        "sex_delta": sex_delta,
        "smoker_delta": smoker_delta,
        "child_delta": child_delta,
    }


def main():
    print("=" * 65)
    print(" MediCalc Pro - Python Syntax Medical Insurance Project")
    print("=" * 65)

    results = run_factor_analysis()

    print(f"\n1. Baseline Insurance Cost (28yo female, BMI 26.2, 3 children, non-smoker):")
    print(f"   -> ${results['baseline_cost']:,.2f}")

    print(f"\n2. Age Factor Sensitivity (+4 years: 28 -> 32):")
    print(f"   -> Delta: +${results['age_delta']:,.2f} (+$250.00 / year)")

    print(f"\n3. BMI Factor Sensitivity (+3.1 BMI: 26.2 -> 29.3):")
    print(f"   -> Delta: +${results['bmi_delta']:,.2f} (+$370.00 / BMI unit)")

    print(f"\n4. Biological Sex Factor (Female [0] -> Male [1]):")
    print(f"   -> Delta: -${abs(results['sex_delta']):,.2f} (-$128.00 adjustment)")

    print(f"\n5. Smoker Factor Sensitivity (Non-smoker [0] -> Smoker [1]):")
    print(f"   -> Delta: +${results['smoker_delta']:,.2f} (Dominant cost driver)")

    print(f"\n6. Dependent Children Factor (+1 child: 3 -> 4):")
    print(f"   -> Delta: +${results['child_delta']:,.2f} (+$425.00 / child)")

    print("\n" + "=" * 65)


if __name__ == "__main__":
    main()
