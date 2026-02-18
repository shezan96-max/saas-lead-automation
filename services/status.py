def determine_status(score : int):
    if score >= 70:
        return "HOT"
    elif score >= 40:
        return "WARM"
    else:
        return "COLD"
    