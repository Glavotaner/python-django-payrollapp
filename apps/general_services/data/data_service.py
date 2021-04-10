def get_period_id(year: int, month: int) -> str:
    return str(year) + str('00' + str(month))[-2:]
