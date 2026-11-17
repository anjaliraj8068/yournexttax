from decimal import Decimal

def _calculate_progressive_tax(income, slabs):
    tax = Decimal("0.0")
    for limit, rate in slabs:
        if income <= 0:
            break
        if limit is None:
            tax += income * rate
            break
        else:
            taxable_amount_in_slab = min(income, limit)
            tax += taxable_amount_in_slab * rate
            income -= taxable_amount_in_slab
    return tax

def add_cess(tax):
    """Adds 4% Health and Education Cess"""
    return tax + (tax * Decimal("0.04"))

def calculate_old_regime_tax(taxable_income):
    """
    Apply Old Regime slabs progressively for FY 2025-26.
    Slabs (Individuals below 60 years):
    Up to Rs 2,50,000 : Nil
    Rs 2,50,001 to Rs 5,00,000 : 5%
    Rs 5,00,001 to Rs 10,00,000 : 20%
    Above Rs 10,00,000 : 30%
    """
    income = max(Decimal(str(taxable_income)), Decimal("0"))
    
    slabs = [
        (Decimal("250000"), Decimal("0.0")),    # Next 2,50,000 (0 to 2,50,000)
        (Decimal("250000"), Decimal("0.05")),   # Next 2,50,000 (2,50,001 to 5,00,000)
        (Decimal("500000"), Decimal("0.20")),   # Next 5,00,000 (5,00,001 to 10,00,000)
        (None, Decimal("0.30"))                 # Above 10,00,000
    ]
    tax = _calculate_progressive_tax(income, slabs)
    
    # Section 87A Rebate for Old Regime
    if income <= Decimal("500000"):
        tax = Decimal("0")
        
    return tax

def calculate_new_regime_tax(total_income):
    """
    Apply New Regime slabs progressively for FY 2025-26 (AY 2026-27).
    Slabs:
    Up to Rs 4,00,000 : Nil
    Rs 4,00,001 to Rs 8,00,000 : 5%
    Rs 8,00,001 to Rs 12,00,000 : 10%
    Rs 12,00,001 to Rs 16,00,000 : 15%
    Rs 16,00,001 to Rs 20,00,000 : 20%
    Rs 20,00,001 to Rs 24,00,000 : 25%
    Above Rs 24,00,000 : 30%
    """
    income = max(Decimal(str(total_income)), Decimal("0"))
    
    slabs = [
        (Decimal("400000"), Decimal("0.0")),    # Next 4,00,000 (0 to 4,00,000)
        (Decimal("400000"), Decimal("0.05")),   # Next 4,00,000 (4,00,001 to 8,00,000)
        (Decimal("400000"), Decimal("0.10")),   # Next 4,00,000 (8,00,001 to 12,00,000)
        (Decimal("400000"), Decimal("0.15")),   # Next 4,00,000 (12,00,001 to 16,00,000)
        (Decimal("400000"), Decimal("0.20")),   # Next 4,00,000 (16,00,001 to 20,00,000)
        (Decimal("400000"), Decimal("0.25")),   # Next 4,00,000 (20,00,001 to 24,00,000)
        (None, Decimal("0.30"))                 # Above 24,00,000
    ]
    tax = _calculate_progressive_tax(income, slabs)

    # Section 87A Rebate for New Regime
    if income <= Decimal("1200000"):
        tax = Decimal("0")

    return tax

def calculate_tax_summary(total_income, total_deduction):
    total_income = Decimal(str(total_income))
    total_deduction = Decimal(str(total_deduction))
    
    # Old Regime: Taxable Income = Total Income - Total Deduction
    taxable_income = max(total_income - total_deduction, Decimal("0"))
    old_tax = calculate_old_regime_tax(taxable_income)
    old_tax = add_cess(old_tax)
    
    # New Regime: Taxable Income = Total Income
    new_tax = calculate_new_regime_tax(total_income)
    new_tax = add_cess(new_tax)
    
    # AI Recommendation Rules
    if old_tax < new_tax:
        better_regime = "Old Regime"
        tax_saving = new_tax - old_tax
        if total_deduction >= Decimal("200000"):
            ai_recommendation = (
                "You have claimed significant deductions. "
                "The Old Regime structure combined with your claims will definitively yield the most tax savings."
            )
        else:
            ai_recommendation = "Based on your deductions, the Old Regime calculates to be more beneficial."
    elif new_tax < old_tax:
        better_regime = "New Regime"
        tax_saving = old_tax - new_tax
        if total_deduction == 0:
            ai_recommendation = (
                "No deductions have been claimed. "
                "The New Regime is inherently beneficial for lower tax outflow without deductions."
            )
        elif total_deduction < Decimal("100000"):
            ai_recommendation = (
                "Because your deductions are relatively low, "
                "the New Regime's improved tax threshold works significantly better for your income."
            )
        else:
            ai_recommendation = "Despite your deductions, the New Regime structure is still more beneficial for you."
    else:
        better_regime = "Both"
        tax_saving = Decimal("0")
        if total_deduction == Decimal("0"):
            ai_recommendation = "No deductions claimed, and both regimes result in the identical tax liability."
        else:
            ai_recommendation = "Both regimes have been compared automatically and yield the exact same tax output."

    # Effective Tax Percentage
    if total_income > Decimal("0"):
        tax_percentage = round((min(old_tax, new_tax) / total_income) * 100, 2)
    else:
        tax_percentage = Decimal("0")

    return {
        "income": total_income,
        "deduction": total_deduction,
        "taxable_income": taxable_income,
        "tax": old_tax,  # Maintained for template backward-compatibility if used
        "old_tax": old_tax,
        "new_tax": new_tax,
        "better_regime": better_regime,
        "tax_saving": tax_saving,
        "tax_percentage": tax_percentage,
        "ai_recommendation": ai_recommendation,
    }
