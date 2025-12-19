from flask import Flask, render_template, request, jsonify
from config import Config
from utils.data_loader import load_hospitals
from services.allocation_engine import rank_hospitals
from rapidfuzz import process
from services.chatbot_service import generate_chatbot_reply


# -------------------------------------------------
# Initialize Flask App
# -------------------------------------------------
app = Flask(__name__)
app.config.from_object(Config)

# -------------------------------------------------
# Load Hospital Dataset Once at Startup
# -------------------------------------------------
try:
    hospitals_df = load_hospitals(Config.DATASET_PATH)
    hospitals_df["city"] = hospitals_df["city"].str.lower().str.strip()
    print("✅ Hospital dataset loaded:", hospitals_df.shape)
except Exception as e:
    print("❌ Failed to load hospital dataset:", e)
    hospitals_df = None


# -------------------------------------------------
# Fuzzy City Matching Helper
# -------------------------------------------------
def get_best_city_match(user_city, available_cities, threshold=70):
    match = process.extractOne(
        user_city,
        available_cities,
        score_cutoff=threshold
    )
    return match[0] if match else None


# -------------------------------------------------
# Home Page
# -------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")


# -------------------------------------------------
# City Autocomplete API
# -------------------------------------------------
@app.route("/cities")
def cities():
    if hospitals_df is None:
        return jsonify([])

    query = request.args.get("q", "").strip().lower()
    if len(query) < 2:
        return jsonify([])

    city_list = hospitals_df["city"].unique().tolist()
    matches = [c for c in city_list if query in c]
    return jsonify(sorted(matches)[:10])


# -------------------------------------------------
# Get States
# -------------------------------------------------
@app.route("/states")
def states():
    if hospitals_df is None:
        return jsonify([])
    return jsonify(sorted(hospitals_df["state"].dropna().unique().tolist()))


# -------------------------------------------------
# Cities by State
# -------------------------------------------------
@app.route("/cities_by_state")
def cities_by_state():
    if hospitals_df is None:
        return jsonify([])

    state = request.args.get("state", "").strip().lower()
    if not state:
        return jsonify([])

    cities = (
        hospitals_df[hospitals_df["state"].str.lower() == state]["city"]
        .dropna()
        .unique()
        .tolist()
    )
    return jsonify(sorted(cities))


# -------------------------------------------------
# Hospital Allocation Route
# -------------------------------------------------
@app.route("/allocate", methods=["POST"])
def allocate():
    if hospitals_df is None:
        return render_template(
            "result.html",
            hospitals=[],
            emergency=None,
            severity="Low",
            error="Hospital dataset not available."
        )

    # ---------- User Input ----------
    raw_city = request.form.get("city", "").strip().lower()

    emergency = request.form.get("emergency", "General").strip()
    severity_input = request.form.get("severity", "1")

    try:
        severity_score = int(severity_input)
    except ValueError:
        severity_score = 1

    # ---------- Severity Mapping (IMPORTANT FIX) ----------
    if severity_score >= 7:
        severity_label = "High"
    elif severity_score >= 4:
        severity_label = "Moderate"
    else:
        severity_label = "Low"

    # ---------- City Matching ----------
    available_cities = hospitals_df["city"].unique().tolist()

    if raw_city not in available_cities:
        corrected_city = get_best_city_match(raw_city, available_cities)
        if corrected_city:
            city = corrected_city
        else:
            return render_template(
                "result.html",
                hospitals=[],
                emergency=emergency,
                severity=severity_label,
                error=f"No matching city found for '{raw_city}'."
            )
    else:
        city = raw_city

    # ---------- Filter Hospitals ----------
    city_hospitals = hospitals_df[hospitals_df["city"] == city]

    if city_hospitals.empty:
        return render_template(
            "result.html",
            hospitals=[],
            emergency=emergency,
            severity=severity_label,
            error=f"No hospitals available in {city.title()}."
        )

    # ---------- Rank Hospitals ----------
    ranked = rank_hospitals(city_hospitals, severity_score, emergency)

    if ranked.empty:
        return render_template(
            "result.html",
            hospitals=[],
            emergency=emergency,
            severity=severity_label,
            error="No suitable hospitals found for this condition."
        )

    # ---------- Final Render ----------
    return render_template(
        "result.html",
        hospitals=ranked.to_dict(orient="records"),
        emergency=emergency,
        severity=severity_label,   # ✅ STRING ONLY
        error=None
    )


# -------------------------------------------------
# Chatbot Route (Safe / Local)
# -------------------------------------------------
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"reply": "Please type a question to continue."})

    # Context from top recommended hospital (if available)
    context = {}
    try:
        if hospitals_df is not None and len(hospitals_df) > 0:
            context = {
                "hospital_name": request.args.get("hospital"),
                "icu_load": request.args.get("icu_load"),
                "icu_beds": request.args.get("icu_beds"),
                "severity": request.args.get("severity"),
                "emergency": request.args.get("emergency")
            }
    except Exception:
        pass

    reply = generate_chatbot_reply(user_message, context)
    return jsonify({"reply": reply})

# -------------------------------------------------
# Run App
# -------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
