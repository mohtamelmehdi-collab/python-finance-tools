"""
=============================================================
finance_tools.py — Python Finance Utilities
Author  : El Mahdi Mohtam
Version : 1.0
Date    : 2025
=============================================================
A collection of beginner-level Python finance functions:
  - Amortization schedule
  - Variance analysis
  - Financial ratio calculator
  - Simple budget tracker

⚠️  SECURITY: All data is FICTITIOUS. No real figures used.
=============================================================
"""

import pandas as pd
from datetime import date


# ─────────────────────────────────────────────
# 1. AMORTIZATION SCHEDULE
# ─────────────────────────────────────────────
def amortization_schedule(cost: float, useful_life: int,
                           method: str = "linear",
                           residual_value: float = 0.0) -> pd.DataFrame:
    """
    Generate a depreciation schedule.

    Parameters:
        cost          : Asset acquisition cost (MAD)
        useful_life   : Useful life in years
        method        : 'linear' or 'declining'
        residual_value: Residual/salvage value at end of life

    Returns:
        DataFrame with annual depreciation schedule
    """
    depreciable_base = cost - residual_value
    rows = []
    book_value = cost

    for year in range(1, useful_life + 1):
        if method == "linear":
            depreciation = depreciable_base / useful_life

        elif method == "declining":
            rate = 2 / useful_life  # Double declining balance
            depreciation = book_value * rate
            # Switch to linear in final years if more favorable
            remaining_years = useful_life - year + 1
            linear_dep = (book_value - residual_value) / remaining_years
            depreciation = max(depreciation, linear_dep)

        else:
            raise ValueError("Method must be 'linear' or 'declining'")

        # Ensure we don't depreciate below residual value
        depreciation = min(depreciation, book_value - residual_value)
        accumulated = cost - book_value + depreciation
        book_value -= depreciation

        rows.append({
            "Year":                year,
            "Opening BV (MAD)":   round(cost - (accumulated - depreciation), 2),
            "Depreciation (MAD)": round(depreciation, 2),
            "Accumulated (MAD)":  round(accumulated, 2),
            "Closing BV (MAD)":   round(book_value, 2),
        })

    return pd.DataFrame(rows).set_index("Year")


# ─────────────────────────────────────────────
# 2. VARIANCE ANALYSIS
# ─────────────────────────────────────────────
def variance_analysis(budget: dict, actual: dict) -> pd.DataFrame:
    """
    Compare budget vs actual by category.

    Parameters:
        budget : dict {category: amount}
        actual : dict {category: amount}

    Returns:
        DataFrame with variance analysis
    """
    categories = set(list(budget.keys()) + list(actual.keys()))
    rows = []

    for cat in sorted(categories):
        b = budget.get(cat, 0)
        a = actual.get(cat, 0)
        variance = b - a
        pct = (variance / b * 100) if b != 0 else None
        status = "✅ Favorable" if variance >= 0 else "🔴 Dépassement"

        rows.append({
            "Catégorie":    cat,
            "Budget (MAD)": b,
            "Réel (MAD)":   a,
            "Écart (MAD)":  variance,
            "Écart (%)":    round(pct, 1) if pct is not None else "N/A",
            "Statut":       status,
        })

    df = pd.DataFrame(rows)

    # Totals row
    totals = {
        "Catégorie":    "TOTAL",
        "Budget (MAD)": df["Budget (MAD)"].sum(),
        "Réel (MAD)":   df["Réel (MAD)"].sum(),
        "Écart (MAD)":  df["Écart (MAD)"].sum(),
        "Écart (%)":    round((df["Écart (MAD)"].sum() / df["Budget (MAD)"].sum()) * 100, 1),
        "Statut":       "✅ Favorable" if df["Écart (MAD)"].sum() >= 0 else "🔴 Dépassement",
    }
    df = pd.concat([df, pd.DataFrame([totals])], ignore_index=True)

    return df


# ─────────────────────────────────────────────
# 3. FINANCIAL RATIOS
# ─────────────────────────────────────────────
def financial_ratios(financials: dict) -> dict:
    """
    Calculate key financial ratios.

    Parameters:
        financials: dict with keys:
            revenue, gross_profit, ebit, net_income,
            total_assets, equity, current_assets,
            current_liabilities, total_debt, ebitda

    Returns:
        dict of calculated ratios
    """
    f = financials
    safe_div = lambda a, b: round(a / b, 4) if b and b != 0 else None

    return {
        # Profitability
        "Gross Margin":     safe_div(f.get("gross_profit"), f.get("revenue")),
        "EBIT Margin":      safe_div(f.get("ebit"), f.get("revenue")),
        "Net Margin":       safe_div(f.get("net_income"), f.get("revenue")),
        "ROA":              safe_div(f.get("net_income"), f.get("total_assets")),
        "ROE":              safe_div(f.get("net_income"), f.get("equity")),

        # Liquidity
        "Current Ratio":    safe_div(f.get("current_assets"), f.get("current_liabilities")),
        "Quick Ratio":      safe_div(
            (f.get("current_assets", 0) - f.get("inventory", 0)),
            f.get("current_liabilities")
        ),

        # Leverage
        "Debt/Equity":      safe_div(f.get("total_debt"), f.get("equity")),
        "Debt/EBITDA":      safe_div(f.get("total_debt"), f.get("ebitda")),
        "Interest Coverage": safe_div(f.get("ebit"), f.get("interest_expense")),
    }


# ─────────────────────────────────────────────
# DEMO / MAIN
# ─────────────────────────────────────────────
if __name__ == "__main__":

    print("\n" + "="*55)
    print("  DEMO: Python Finance Tools")
    print("  ⚠️  All data is FICTITIOUS")
    print("="*55)

    # --- 1. Depreciation ---
    print("\n📊 1. DEPRECIATION SCHEDULE (Linear Method)")
    print("   Asset: Industrial Equipment | Cost: 500,000 MAD | Life: 5 years")
    schedule = amortization_schedule(cost=500_000, useful_life=5, method="linear")
    print(schedule.to_string())

    # --- 2. Variance Analysis ---
    print("\n📊 2. VARIANCE ANALYSIS — Budget vs Réel")
    budget_data = {
        "Matières premières":  120_000,
        "Main d'oeuvre":        80_000,
        "Charges indirectes":   40_000,
        "Frais généraux":       20_000,
    }
    actual_data = {
        "Matières premières":  115_000,
        "Main d'oeuvre":        85_000,
        "Charges indirectes":   38_000,
        "Frais généraux":       22_000,
    }
    va = variance_analysis(budget_data, actual_data)
    print(va.to_string(index=False))

    # --- 3. Financial Ratios ---
    print("\n📊 3. FINANCIAL RATIOS")
    fin = {
        "revenue":             200_000_000,
        "gross_profit":         60_000_000,
        "ebit":                 30_000_000,
        "ebitda":               36_000_000,
        "net_income":           20_000_000,
        "total_assets":        150_000_000,
        "equity":               80_000_000,
        "current_assets":       50_000_000,
        "current_liabilities":  25_000_000,
        "inventory":            10_000_000,
        "total_debt":           40_000_000,
        "interest_expense":      2_000_000,
    }
    ratios = financial_ratios(fin)
    for k, v in ratios.items():
        print(f"  {k:<22}: {v:.2%}" if isinstance(v, float) and v < 10
              else f"  {k:<22}: {v}")

    print("\n✅ Done.\n")
