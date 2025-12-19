def score_hospital(hospital, severity, emergency_type):
    score = 0

    # ICU availability
    if hospital["icu_beds"] > 0:
        score += 30

    # Emergency specialization
    if emergency_type == "Cardiac" and hospital["cardiac_unit"] == "Yes":
        score += 25

    if emergency_type == "Trauma" and hospital["trauma_unit"] == "Yes":
        score += 25

    if emergency_type == "Burn" and hospital["burn_unit"] == "Yes":
        score += 25

    # Load penalty
    if hospital["current_icu_load_percent"] < 80:
        score += 15
    else:
        score -= 10

    # Severity priority
    score += severity * 2

    return score


def rank_hospitals(df, severity, emergency_type, top_n=5):
    if df.empty:
        return df

    df = df.copy()
    df["score"] = df.apply(
        lambda row: score_hospital(row, severity, emergency_type),
        axis=1
    )

    return df.sort_values(by="score", ascending=False).head(top_n)
