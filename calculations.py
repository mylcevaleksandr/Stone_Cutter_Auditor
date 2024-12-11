def calculate_square_meters(width_mm: int, length_mm: int) -> float:
    width_cm = width_mm / 10
    length_cm = length_mm / 10
    area_cm2 = width_cm * length_cm
    area_m2 = area_cm2 / 10000
    area_m2_formatted = format(area_m2, '.2f')
    return float(area_m2_formatted)