"""
Medicare Command Center & Interactive Field Assistant
Python-based Medicare Knowledge Engine with full dictionary lookup,
actuarial calculations, Bankers Life sales scripts, and allowed commands.
"""

import sys
import json
import math
from typing import List, Dict, Any, Optional

# Ensure UTF-8 output on Windows consoles if supported
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

import medicare_dictionary as md


class MedicareAssistant:
    def __init__(self):
        self.dict_data = md.GLOSSARY
        self.parts = md.MEDICARE_PARTS
        self.magic_numbers = md.MAGIC_NUMBERS
        self.irmaa_tiers = md.IRMAA_TIERS_2026
        self.enrollment_periods = md.ENROLLMENT_PERIODS
        self.medigap_matrix = md.MEDIGAP_MATRIX
        self.sales_scripts = md.SALES_SCRIPTS
        self.checkpoints = md.CHECKPOINTS_QA
        self.commands = md.ALLOWED_COMMANDS

    # --------------------------------------------------------------------------
    # COMMAND ROUTING & DISPATCH
    # --------------------------------------------------------------------------
    def execute_command(self, cmd_line: str) -> bool:
        """
        Execute a command line string. Returns False if user wishes to exit.
        """
        parts = cmd_line.strip().split()
        if not parts:
            return True

        cmd = parts[0].lower()
        args = parts[1:]

        # Handle aliases
        for canonical, spec in self.commands.items():
            if cmd == canonical or cmd in spec.get("aliases", []):
                cmd = canonical
                break

        if cmd in ["exit", "quit", "q"]:
            print("\nExiting Medicare Assistant. Have a productive day in the field!")
            return False

        elif cmd == "help":
            self.cmd_help(args)

        elif cmd == "dict":
            self.cmd_dict(args)

        elif cmd == "terms":
            self.cmd_terms()

        elif cmd == "magic":
            self.cmd_magic()

        elif cmd == "calc-part-a":
            self.cmd_calc_part_a(args)

        elif cmd == "calc-snf":
            self.cmd_calc_snf(args)

        elif cmd == "calc-part-b":
            self.cmd_calc_part_b(args)

        elif cmd == "calc-ppsp":
            self.cmd_calc_ppsp(args)

        elif cmd == "calc-irmaa":
            self.cmd_calc_irmaa(args)

        elif cmd == "calc-penalty-d":
            self.cmd_calc_penalty_d(args)

        elif cmd == "calc-total":
            self.cmd_calc_total(args)

        elif cmd == "script":
            self.cmd_script(args)

        elif cmd == "plan":
            self.cmd_plan(args)

        elif cmd == "periods":
            self.cmd_periods(args)

        elif cmd == "checkpoint":
            self.cmd_checkpoint(args)

        elif cmd == "quiz":
            self.cmd_quiz()

        elif cmd == "export-json":
            self.cmd_export_json(args)

        else:
            print(f"Unknown command: '{cmd}'. Type 'help' to view all allowed commands.")

        return True

    # --------------------------------------------------------------------------
    # COMMAND HANDLERS
    # --------------------------------------------------------------------------
    def cmd_help(self, args: List[str]):
        if args:
            target = args[0].lower()
            for name, info in self.commands.items():
                if target == name or target in info.get("aliases", []):
                    print(f"\nCOMMAND: {name.upper()}")
                    print(f"Syntax:      {info['syntax']}")
                    print(f"Description: {info['desc']}")
                    print(f"Example:     {info['example']}")
                    if "aliases" in info:
                        print(f"Aliases:     {', '.join(info['aliases'])}")
                    print()
                    return
            print(f"No specific help found for '{target}'.")
            return

        print("\n" + "=" * 70)
        print(" MEDICARE ASSISTANT - ALLOWED COMMANDS SPECIFICATION")
        print("=" * 70)
        for name, info in self.commands.items():
            aliases = f" (aliases: {', '.join(info['aliases'])})" if "aliases" in info else ""
            print(f" {name:<15}{aliases}")
            print(f"   Usage: {info['syntax']}")
            print(f"   Desc:  {info['desc']}\n")
        print("Tip: Run 'help <command>' for specific syntax and examples.")
        print("=" * 70 + "\n")

    def cmd_magic(self):
        print("\n" + "=" * 70)
        print(" [*] THE 5 MAGIC NUMBERS & ESSENTIAL FIELD METRICS (Bankers Life 2026)")
        print("=" * 70)
        print(f" 1. Part A Hospital Deductible:    ${self.magic_numbers['PART_A_DEDUCTIBLE']:,.2f} / Benefit Period")
        print("    |-- Divisible by 2 rule:")
        print(f"        * Days 91-150 Copay:       ${self.magic_numbers['PART_A_DEDUCTIBLE']/2:,.2f} / day")
        print(f"        * Days 61-90 Copay:        ${self.magic_numbers['PART_A_DEDUCTIBLE']/4:,.2f} / day")
        print(f"        * SNF Days 21-100 Copay:   ${self.magic_numbers['PART_A_DEDUCTIBLE']/8:,.2f} / day")
        print(f" 2. Part B Standard Premium:      ${self.magic_numbers['PART_B_PREMIUM']:,.2f} / month (Deducted from SSA)")
        print(f" 3. Part B Annual Deductible:      ${self.magic_numbers['PART_B_DEDUCTIBLE']:,.2f} / calendar year")
        print(f" 4. First IRMAA Tier Threshold:    ${self.magic_numbers['IRMAA_TIER_1_SINGLE']:,.2f} Single / ${self.magic_numbers['IRMAA_TIER_1_MARRIED']:,.2f} Married")
        print(f" 5. Bankers Life PPSP Formula:     (Annual Premium x 0.08583) + $1.00 = Monthly EFT")
        print("-" * 70)
        print(f" - Part D Out-of-Pocket Cap:       ${self.magic_numbers['PART_D_OOP_CAP']:,.2f} / year (2026 Inflation Reduction Act)")
        print(f" - Part D National Base Premium:   ${self.magic_numbers['PART_D_BASE_PREMIUM']:,.2f} (Base for 1%/mo penalty)")
        print(f" - Maximum Monthly Insulin Copay:  ${self.magic_numbers['INSULIN_MONTHLY_CAP']:,.2f} / month")
        print(" - Core Distinction:               'Medicare is CARE for the OLD; Medicaid is AID for the POOR'")
        print("=" * 70 + "\n")

    def cmd_dict(self, args: List[str]):
        if not args:
            print("Usage: dict <term> (e.g. 'dict IRMAA', 'dict assignment', 'dict Part A')")
            return

        query = " ".join(args).lower().strip()
        matches = []

        # Check glossary
        for key, item in self.dict_data.items():
            if query == key.lower() or query in item["term"].lower() or query in item["def"].lower():
                matches.append((item["term"], item["def"]))

        # Check parts
        for part_key, part_info in self.parts.items():
            if query in part_key.lower() or query in part_info["title"].lower():
                matches.append((f"{part_key}: {part_info['title']}", part_info["summary"]))

        if not matches:
            print(f"No definition found matching '{query}'. Run 'terms' to see all dictionary terms.")
            return

        print("\n" + "-" * 70)
        for term, definition in matches:
            print(f"[DEFINITION] {term.upper()}")
            print(f"   {definition}\n")
        print("-" * 70)

    def cmd_terms(self):
        print("\n" + "=" * 70)
        print(" MEDICARE DICTIONARY AVAILABLE TERMS")
        print("=" * 70)
        categories = {
            "Core Parts": ["Part A", "Part B", "Part C", "Part D", "Medigap"],
            "Legal & Operations": ["Assignment", "ACO", "Benefit Period", "Creditable Coverage", "Guaranteed Issue Rights", "MBI", "MOON"],
            "Cost Sharing": ["Coinsurance", "Copayment", "DME", "Formulary", "IRMAA", "Lifetime Reserve Days", "PPSP"],
            "Programs & Facilities": ["Medicaid", "SNF"]
        }
        for cat, items in categories.items():
            print(f"\n[{cat}]")
            for item in items:
                print(f"  * {item:<24} -> dict {item.lower()}")
        print("\n" + "=" * 70 + "\n")

    def cmd_calc_part_a(self, args: List[str]):
        if not args:
            print("Usage: calc-part-a <days_in_hospital> (e.g. 'calc-part-a 75')")
            return
        try:
            days = int(args[0])
            if days <= 0:
                print("Days must be greater than 0.")
                return
        except ValueError:
            print("Invalid number of days.")
            return

        deductible = self.magic_numbers["PART_A_DEDUCTIBLE"]
        days_61_90_rate = deductible / 4  # $434
        days_91_150_rate = deductible / 2  # $868

        total_cost = deductible
        reserve_days_used = 0

        breakdown = [f"* Days 1–{min(days, 60)}: Covered under initial Part A Deductible (${deductible:,.2f})"]

        if days > 60:
            tier2_days = min(days, 90) - 60
            tier2_cost = tier2_days * days_61_90_rate
            total_cost += tier2_cost
            breakdown.append(f"* Days 61–{min(days, 90)} ({tier2_days} days x ${days_61_90_rate:,.2f}/day): ${tier2_cost:,.2f}")

        if days > 90:
            reserve_days_used = min(days, 150) - 90
            reserve_cost = reserve_days_used * days_91_150_rate
            total_cost += reserve_cost
            breakdown.append(f"* Days 91–{min(days, 150)} ({reserve_days_used} lifetime reserve days x ${days_91_150_rate:,.2f}/day): ${reserve_cost:,.2f}")

        if days > 150:
            uncovered_days = days - 150
            breakdown.append(f"* Days 151+ ({uncovered_days} days): 100% UNCOVERED by Medicare! Patient pays all hospital room and board charges.")

        print("\n" + "=" * 70)
        print(f" MEDICARE PART A INPATIENT HOSPITAL CALCULATION ({days} DAYS)")
        print("=" * 70)
        for item in breakdown:
            print(f" {item}")
        print("-" * 70)
        print(f" Total Patient Coinsurance & Deductible Liability: ${total_cost:,.2f}")
        print(f" Lifetime Reserve Days Used:                       {reserve_days_used} of 60 days (Remaining: {60 - reserve_days_used})")
        print(f" Medigap Plan G Protection:                        Covers 100% of deductible + coinsurance ($0 patient cost)")
        print("=" * 70 + "\n")

    def cmd_calc_snf(self, args: List[str]):
        if not args:
            print("Usage: calc-snf <rehab_days> (e.g. 'calc-snf 45')")
            return
        try:
            days = int(args[0])
            if days <= 0:
                print("Days must be greater than 0.")
                return
        except ValueError:
            print("Invalid number of days.")
            return

        snf_daily_coinsurance = self.magic_numbers["PART_A_DEDUCTIBLE"] / 8  # $217.00
        total_cost = 0.0

        print("\n" + "=" * 70)
        print(f" SKILLED NURSING FACILITY (SNF) REHABILITATION CALCULATION ({days} DAYS)")
        print("=" * 70)
        print(" Prerequisite Check:")
        print("   [+] Requires 3 consecutive inpatient hospital nights prior to transfer")
        print("   [+] Must enter SNF within 30 days of hospital discharge for the same condition")
        print("-" * 70)

        if days <= 20:
            print(f" * Days 1–{days}: Covered 100% by Medicare ($0 patient cost)")
            total_cost = 0.0
        else:
            print(" * Days 1–20: Covered 100% by Medicare ($0 patient cost)")
            coinsurance_days = min(days, 100) - 20
            coinsurance_cost = coinsurance_days * snf_daily_coinsurance
            total_cost += coinsurance_cost
            print(f" * Days 21–{min(days, 100)}: {coinsurance_days} days x ${snf_daily_coinsurance:,.2f}/day = ${coinsurance_cost:,.2f}")

            if days > 100:
                uncovered_days = days - 100
                print(f" * Days 101+: {uncovered_days} days UNCOVERED by Medicare! (100% private pay / Long-Term Care needed)")

        print("-" * 70)
        print(f" Total Patient Out-of-Pocket Liability: ${total_cost:,.2f}")
        print(f" Medigap (Plans C, D, F, G, M, N) Coverage: 100% of Day 21–100 coinsurance covered ($0 out-of-pocket)")
        print("=" * 70 + "\n")

    def cmd_calc_part_b(self, args: List[str]):
        if not args:
            print("Usage: calc-part-b <annual_bills> (e.g. 'calc-part-b 4000')")
            return
        try:
            bills = float(args[0])
            if bills < 0:
                print("Bills cannot be negative.")
                return
        except ValueError:
            print("Invalid amount.")
            return

        deductible = self.magic_numbers["PART_B_DEDUCTIBLE"]  # $283
        if bills <= deductible:
            patient_pays = bills
            medicare_pays = 0.0
            remaining_deductible = deductible - bills
        else:
            subject_to_coinsurance = bills - deductible
            medicare_pays = subject_to_coinsurance * 0.80
            patient_coinsurance = subject_to_coinsurance * 0.20
            patient_pays = deductible + patient_coinsurance
            remaining_deductible = 0.0

        print("\n" + "=" * 70)
        print(f" MEDICARE PART B ANNUAL OUTPATIENT COST BREAKDOWN")
        print(f" Total Approved Medical Bills: ${bills:,.2f}")
        print("=" * 70)
        print(f" * Annual Part B Deductible:    ${deductible:,.2f}")
        print(f" * Deductible Paid by Patient:  ${min(bills, deductible):,.2f}")
        if bills > deductible:
            print(f" * Amount Subject to 80/20:     ${(bills - deductible):,.2f}")
            print(f" * Medicare Share (80%):        ${medicare_pays:,.2f}")
            print(f" * Patient Coinsurance (20%):   ${(bills - deductible) * 0.20:,.2f}")
        print("-" * 70)
        print(f" Total Paid by Medicare:        ${medicare_pays:,.2f}")
        print(f" Total Paid by Patient:         ${patient_pays:,.2f}")
        print(f" Medigap Plan G Protection:     Pays 100% of the 20% coinsurance (Patient pays only $283 deductible)")
        print("=" * 70 + "\n")

    def cmd_calc_ppsp(self, args: List[str]):
        if not args:
            print("Usage: calc-ppsp <annual_premium> (e.g. 'calc-ppsp 1850')")
            return
        try:
            annual = float(args[0])
            if annual <= 0:
                print("Annual premium must be greater than 0.")
                return
        except ValueError:
            print("Invalid annual premium amount.")
            return

        multiplier = self.magic_numbers["PPSP_MULTIPLIER"]
        fee = self.magic_numbers["PPSP_FEE"]
        monthly = (annual * multiplier) + fee

        print("\n" + "=" * 70)
        print(" BANKERS LIFE PPSP MONTHLY EFT PREMIUM CALCULATION")
        print("=" * 70)
        print(" Field Sticky Note Formula: (Annual Premium x 0.08583) + $1.00")
        print(f" * Annual Policy Premium:     ${annual:,.2f}")
        print(f" * Multiplied by 0.08583:     ${annual * multiplier:,.2f}")
        print(f" * Added $1.00 Administrative Fee: $1.00")
        print("-" * 70)
        print(f" [★] Monthly PPSP Bank Draft:  ${monthly:,.2f} / month")
        print("=" * 70 + "\n")

    def cmd_calc_irmaa(self, args: List[str]):
        if len(args) < 2:
            print("Usage: calc-irmaa <modified_agi> <single|married> (e.g. 'calc-irmaa 145000 single')")
            return
        try:
            income = float(args[0])
            status = args[1].lower()
            if status not in ["single", "married", "joint"]:
                print("Status must be 'single' or 'married'.")
                return
        except ValueError:
            print("Invalid income value.")
            return

        selected_tier = None
        for tier in self.irmaa_tiers:
            low, high = tier["single_magi"] if status == "single" else tier["married_magi"]
            if low <= income <= high:
                selected_tier = tier
                break

        if not selected_tier:
            selected_tier = self.irmaa_tiers[-1]

        print("\n" + "=" * 70)
        print(f" 2026 IRMAA SURCHARGE CALCULATION ({status.upper()} - ${income:,.2f})")
        print("=" * 70)
        print(f" * Income Tier Level:             Tier {selected_tier['tier']} of 6")
        print(f" * Standard Part B Base:          ${self.magic_numbers['PART_B_PREMIUM']:,.2f} / month")
        print(f" * Part B IRMAA Surcharge:        +${selected_tier['part_b_surcharge']:,.2f} / month")
        print(f" * Total Monthly Part B Premium:  ${selected_tier['part_b_total']:,.2f} / month")
        print(f" * Part D IRMAA Surcharge:        +${selected_tier['part_d_surcharge']:,.2f} / month (in addition to plan premium)")
        print("-" * 70)
        total_monthly_extra = selected_tier["part_b_surcharge"] + selected_tier["part_d_surcharge"]
        print(f" Total Monthly IRMAA Impact:      +${total_monthly_extra:,.2f} / month (+${total_monthly_extra * 12:,.2f} / year)")
        print(" Note: IRMAA uses tax return from 2 years prior (2026 IRMAA uses 2024 tax return).")
        print("=" * 70 + "\n")

    def cmd_calc_penalty_d(self, args: List[str]):
        if not args:
            print("Usage: calc-penalty-d <uncovered_months> (e.g. 'calc-penalty-d 36')")
            return
        try:
            months = int(args[0])
            if months < 0:
                print("Months cannot be negative.")
                return
        except ValueError:
            print("Invalid number of months.")
            return

        base_premium = self.magic_numbers["PART_D_BASE_PREMIUM"]  # $38.99 in 2026
        # 1% per month
        penalty_pct = months * 0.01
        raw_penalty = penalty_pct * base_premium
        # Rounded to nearest 10 cents
        monthly_penalty = round(raw_penalty, 1)

        print("\n" + "=" * 70)
        print(f" MEDICARE PART D LATE ENROLLMENT PENALTY ({months} UNCOVERED MONTHS)")
        print("=" * 70)
        print(f" * 2026 National Base Beneficiary Premium: ${base_premium:,.2f}")
        print(f" * Penalty Calculation Formula:           {months}% of ${base_premium:,.2f}")
        print(f" * Unrounded Monthly Amount:               ${raw_penalty:.4f}")
        print(f" * Rounded to Nearest $0.10:              ${monthly_penalty:,.2f}")
        print("-" * 70)
        print(f" [★] Permanent Lifetime Surcharge:         +${monthly_penalty:,.2f} / month")
        print(f"     Annualized Extra Cost:                +${monthly_penalty * 12:,.2f} / year for life")
        print(" Case Study Lesson (Barbara from training):")
        print("   Refused $4/mo plan; incurred $12.63/mo permanent penalty 3 years later.")
        print("=" * 70 + "\n")

    def cmd_calc_total(self, args: List[str]):
        if len(args) < 5:
            print("Usage: calc-total <hospital_days> <snf_days> <doctor_bills> <income> <single|married>")
            print("Example: calc-total 10 30 4000 85000 single")
            return
        try:
            h_days = int(args[0])
            s_days = int(args[1])
            b_bills = float(args[2])
            income = float(args[3])
            status = args[4].lower()
        except ValueError:
            print("Invalid arguments format.")
            return

        # Part A
        part_a_cost = self.magic_numbers["PART_A_DEDUCTIBLE"]
        if h_days > 60:
            part_a_cost += (min(h_days, 90) - 60) * (self.magic_numbers["PART_A_DEDUCTIBLE"] / 4)
        if h_days > 90:
            part_a_cost += (min(h_days, 150) - 90) * (self.magic_numbers["PART_A_DEDUCTIBLE"] / 2)

        # SNF
        snf_cost = 0.0
        if s_days > 20:
            snf_cost += (min(s_days, 100) - 20) * (self.magic_numbers["PART_A_DEDUCTIBLE"] / 8)

        # Part B
        part_b_ded = self.magic_numbers["PART_B_DEDUCTIBLE"]
        if b_bills <= part_b_ded:
            part_b_patient = b_bills
        else:
            part_b_patient = part_b_ded + (b_bills - part_b_ded) * 0.20

        # IRMAA
        selected_tier = self.irmaa_tiers[0]
        for tier in self.irmaa_tiers:
            low, high = tier["single_magi"] if status == "single" else tier["married_magi"]
            if low <= income <= high:
                selected_tier = tier
                break
        annual_b_premium = selected_tier["part_b_total"] * 12
        annual_irmaa_d = selected_tier["part_d_surcharge"] * 12

        total_patient = part_a_cost + snf_cost + part_b_patient + annual_b_premium + annual_irmaa_d

        print("\n" + "=" * 70)
        print(" COMPREHENSIVE ANNUAL MEDICARE OUT-OF-POCKET SIMULATION")
        print("=" * 70)
        print(f" 1. Part A Hospital ({h_days} days):               ${part_a_cost:,.2f}")
        print(f" 2. SNF Rehab Care ({s_days} days):                ${snf_cost:,.2f}")
        print(f" 3. Part B Medical Costs (${b_bills:,.2f} billed):  ${part_b_patient:,.2f}")
        print(f" 4. Annual Part B Premiums:                ${annual_b_premium:,.2f} (${selected_tier['part_b_total']:,.2f}/mo)")
        if annual_irmaa_d > 0:
            print(f" 5. Annual Part D IRMAA Surcharge:         ${annual_irmaa_d:,.2f}")
        print("-" * 70)
        print(f" [★] TOTAL ESTIMATED ANNUAL PATIENT OUT-OF-POCKET: ${total_patient:,.2f}")
        print("-" * 70)
        print(" WITH A BANKERS LIFE PLAN G SUPPLEMENT:")
        print(f" * Part A Deductible & Days 61-150: Covered 100% ($0)")
        print(f" * SNF Days 21-100 Coinsurance:     Covered 100% ($0)")
        print(f" * Part B 20% Coinsurance:          Covered 100% ($0)")
        print(f" * Total Medical Liability:         Only ${part_b_ded:,.2f} Part B Deductible!")
        print("=" * 70 + "\n")

    def cmd_script(self, args: List[str]):
        if not args:
            print("Available scripts:")
            print("  turning65, working65, under65, socialsecurity, assumptive, trial, compliance, bridge")
            print("Usage: script <name> (e.g. 'script socialsecurity')")
            return

        choice = args[0].lower().replace("-", "").replace("_", "")
        mapping = {
            "turning65": "scenario_a_turning_65",
            "iep": "scenario_a_turning_65",
            "working65": "scenario_b_working_past_65",
            "sep": "scenario_b_working_past_65",
            "under65": "scenario_c_under_65",
            "socialsecurity": "social_security_close",
            "tchart": "social_security_close",
            "assumptive": "assumptive_close",
            "trial": "trial_close",
            "compliance": "compliance_notice",
            "form6862": "compliance_notice",
            "bridge": "fact_finder_bridge"
        }

        key = mapping.get(choice)
        if not key or key not in self.sales_scripts:
            print(f"Script '{choice}' not found. Choose from: turning65, working65, under65, socialsecurity, assumptive, trial, compliance, bridge.")
            return

        item = self.sales_scripts[key]
        print("\n" + "=" * 70)
        print(f" [SCRIPT] {item['title'].upper()}")
        print("=" * 70)
        if "prospect" in item:
            print(f"Prospect: \"{item['prospect']}\"\n")
        if "agent" in item:
            print(f"Agent Script:\n\"{item['agent']}\"\n")
        if "dialogue" in item:
            print(f"Dialogue:\n\"{item['dialogue']}\"\n")
        if "script" in item:
            print(f"Script:\n\"{item['script']}\"\n")
        print("=" * 70 + "\n")

    def cmd_plan(self, args: List[str]):
        if not args:
            print("Usage: plan <A|B|C|D|F|G|K|L|M|N|compare|all>")
            return

        sub = args[0].upper().strip()
        if sub in ["ALL", "COMPARE"]:
            print("\n" + "=" * 90)
            print(" STANDARDIZED MEDIGAP PLANS BENEFIT MATRIX (2026)")
            print("=" * 90)
            headers = ["Plan", "Part A Ded", "Part B Ded", "Part B Co-ins", "Part B Excess", "SNF Co-ins", "Foreign Trv"]
            print(f" {headers[0]:<8}{headers[1]:<12}{headers[2]:<12}{headers[3]:<15}{headers[4]:<15}{headers[5]:<12}{headers[6]:<12}")
            print("-" * 90)
            for p_name, b in self.medigap_matrix.items():
                print(f" {p_name:<8}{b['part_a_deductible']:<12}{b['part_b_deductible']:<12}{b['part_b_coinsurance'][:13]:<15}{b['part_b_excess']:<15}{b['snf_coinsurance']:<12}{b['foreign_travel']:<12}")
            print("=" * 90)
            print(" Note: Plan G is the primary comprehensive recommendation for newly eligible seniors.")
            print("       Plans C and F are discontinued for enrollees turning 65 after Jan 1, 2020.\n")
            return

        key = f"Plan {sub}" if not sub.startswith("PLAN") else sub.title()
        if key not in self.medigap_matrix:
            print(f"Invalid plan '{sub}'. Valid lettered plans: A, B, C, D, F, G, K, L, M, N.")
            return

        info = self.medigap_matrix[key]
        print("\n" + "=" * 70)
        print(f" [PLAN SPECIFICATION] {key.upper()}")
        print("=" * 70)
        for k, v in info.items():
            print(f" * {k.replace('_', ' ').title():<28}: {v}")
        print("=" * 70 + "\n")

    def cmd_periods(self, args: List[str]):
        if args:
            code = args[0].upper().replace("-", "_")
            if code in self.enrollment_periods:
                p = self.enrollment_periods[code]
                print(f"\n[{p['name']} ({code})]")
                print(f"Duration:  {p['duration']}")
                print(f"Timeline:  {p['timeline']}")
                if "rules" in p: print(f"Rules:     {p['rules']}")
                if "privilege" in p: print(f"Privilege: {p['privilege']}")
                if "risk" in p: print(f"Risk:      {p['risk']}")
                print()
                return

        print("\n" + "=" * 70)
        print(" MEDICARE ENROLLMENT PERIODS DIRECTORY")
        print("=" * 70)
        for code, p in self.enrollment_periods.items():
            print(f" [*] {code} - {p['name']}")
            print(f"     Duration:  {p['duration']}")
            print(f"     Timeline:  {p['timeline']}")
            if "rules" in p:
                print(f"     Details:   {p['rules']}")
            print()
        print("=" * 70 + "\n")

    def cmd_checkpoint(self, args: List[str]):
        if not args or args[0].lower() == "all":
            print("\n" + "=" * 70)
            print(" BANKERS LIFE PARTICIPANT GUIDE CHECKPOINT QUESTIONS (1 to 18)")
            print("=" * 70)
            for num, qa in self.checkpoints.items():
                print(f" Q{num}: {qa['q']}")
                print(f" Ans: {qa['a']}\n")
            print("=" * 70 + "\n")
            return

        try:
            num = int(args[0])
            if num not in self.checkpoints:
                print("Question number must be between 1 and 18.")
                return
            qa = self.checkpoints[num]
            print(f"\n[Checkpoint Question {num}]")
            print(f"Q: {qa['q']}")
            print(f"A: {qa['a']}\n")
        except ValueError:
            print("Invalid checkpoint question number.")

    def cmd_quiz(self):
        print("\n" + "=" * 70)
        print(" [*] MEDICARE AGENT CHECKPOINT TRAINING QUIZ")
        print("=" * 70)
        questions = [
            ("What is the 2026 Medicare Part A hospital deductible per benefit period?", "1736"),
            ("What is the standard 2026 monthly Part B premium?", "202.90"),
            ("What is the 2026 annual Medicare Part B deductible?", "283"),
            ("How many months is the Initial Enrollment Period (IEP)?", "7"),
            ("In the Bankers Life PPSP formula, what is the annual multiplier?", "0.08583")
        ]
        score = 0
        for i, (q, correct) in enumerate(questions, 1):
            print(f"\nQuestion {i}: {q}")
            ans = input("Your Answer: ").strip().replace("$", "").replace(",", "")
            if ans == correct:
                print(">> Correct!")
                score += 1
            else:
                print(f">> Incorrect. Correct answer: {correct}")
        print("\n" + "-" * 70)
        print(f"Quiz Completed! Score: {score}/{len(questions)} ({score/len(questions)*100:.0f}%)")
        print("=" * 70 + "\n")

    def cmd_export_json(self, args: List[str]):
        filename = args[0] if args else "medicare_dictionary.json"
        export_data = {
            "magic_numbers": self.magic_numbers,
            "parts": self.parts,
            "irmaa_tiers": self.irmaa_tiers,
            "enrollment_periods": self.enrollment_periods,
            "medigap_matrix": self.medigap_matrix,
            "sales_scripts": self.sales_scripts,
            "checkpoint_qa": self.checkpoints,
            "glossary": self.dict_data,
            "allowed_commands": self.commands
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(export_data, f, indent=2)
        print(f"\n[+] Successfully exported complete Medicare database to: {filename}\n")

    def run_interactive(self):
        print("=" * 70)
        print(" MEDICARE COMMAND CENTER & FIELD ASSISTANT (2026)")
        print(" Bankers Life Sales Essentials & CMS Standards System")
        print("=" * 70)
        print("Type 'help' to view all allowed commands, or 'magic' for key numbers.")
        print("Type 'exit' to quit.\n")

        while True:
            try:
                line = input("Medicare [2026]> ")
                if not self.execute_command(line):
                    break
            except (KeyboardInterrupt, EOFError):
                print("\nSession ended.")
                break


def main():
    assistant = MedicareAssistant()
    if len(sys.argv) > 1:
        # Run command directly from CLI arguments
        cmd_str = " ".join(sys.argv[1:])
        assistant.execute_command(cmd_str)
    else:
        # Launch interactive REPL shell
        assistant.run_interactive()


if __name__ == "__main__":
    main()
