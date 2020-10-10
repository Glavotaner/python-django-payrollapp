# INCOME TAX CALCULATION
def calculate_income_tax_amount_young(current_tax_model: object, tax_base: float) -> float:

    if tax_base > current_tax_model.tax_bracket:
        hi_tax_base = tax_base - \
            current_tax_model.tax_bracket

        income_tax = (current_tax_model.tax_bracket *
                      current_tax_model.lo_tax_rate) + \
            (hi_tax_base * current_tax_model.hi_tax_rate)

    else:
        income_tax = tax_base * \
            current_tax_model.lo_tax_rate

    return round(income_tax / 2, 2)


def calculate_income_tax_amount(current_tax_model: object, tax_base: float) -> float:

    if tax_base > current_tax_model.tax_bracket:
        hi_tax_base = tax_base - \
            current_tax_model.tax_bracket

        income_tax = (current_tax_model.tax_bracket *
                      current_tax_model.lo_tax_rate) + \
            (hi_tax_base * current_tax_model.hi_tax_rate)

    else:
        income_tax = tax_base * \
            current_tax_model.lo_tax_rate

    return round(income_tax, 2)


def calculate_city_tax_amount(income_tax_amount: float, city: object) -> float:
    return round(income_tax_amount * (city.tax_rate -
                                      city.tax_break), 2)


def calculate_tax_amount(income_tax_amount: float, city_tax_amount: float) -> float:
    return round(income_tax_amount + city_tax_amount, 2)
