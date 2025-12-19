def generate_chatbot_reply(message, context=None):
    """
    Context-aware medical guidance chatbot.
    Safe, deterministic, and suitable for healthcare demos.
    """

    msg = message.lower().strip()
    ctx = context or {}

    hospital = ctx.get("hospital_name", "the recommended hospital")
    icu_load = ctx.get("icu_load")
    icu_beds = ctx.get("icu_beds")
    severity = ctx.get("severity", "the assessed level")
    emergency = ctx.get("emergency", "your condition")

    # --- WHY THIS HOSPITAL ---
    if any(k in msg for k in ["why", "recommended", "selected"]):
        return (
            f"{hospital} was recommended because it offers appropriate care for "
            f"{emergency} with manageable ICU load"
            f"{f' ({icu_load}% occupied)' if icu_load is not None else ''}, "
            "ensuring quicker admission and better monitoring."
        )

    # --- ICU EXPLANATION ---
    if "icu" in msg or "bed" in msg:
        return (
            f"ICU load indicates how many ICU beds are currently occupied. "
            f"{hospital} has "
            f"{f'{icu_beds} ICU beds available' if icu_beds else 'adequate ICU capacity'}, "
            "which improves chances of immediate care."
        )

    # --- SEVERITY ---
    if "severity" in msg or "serious" in msg:
        return (
            f"The severity level is assessed as {severity}. "
            "This helps prioritize hospitals that can provide the required level of care "
            "without unnecessary delay."
        )

    # --- WHAT SHOULD I DO NOW ---
    if any(k in msg for k in ["what next", "what should i do", "next step", "now what"]):
        return (
            "Please proceed to the recommended hospital as soon as possible. "
            "Carry previous medical reports, current medications, and ensure "
            "someone accompanies the patient if possible."
        )

    # --- EMERGENCY SAFETY ---
    if any(k in msg for k in ["emergency", "urgent", "critical"]):
        return (
            "If symptoms worsen or the patient becomes unresponsive, "
            "seek emergency medical care immediately or call local emergency services."
        )

    # --- FALLBACK ---
    return (
        "I can help explain hospital recommendations, ICU availability, "
        "severity levels, and next steps. "
        "Please ask your question."
    )
