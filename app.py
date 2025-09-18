from flask import Flask, render_template, request, jsonify
from healthcare_data import DISEASE_DB
import re
from difflib import get_close_matches
import traceback

# Try to support multiple googlesearch package signatures
try:
    from googlesearch import search as google_search
except Exception:
    google_search = None

app = Flask(__name__)


def normalize_text(s: str) -> str:
    """Lowercase and keep only alphanumerics and spaces."""
    return re.sub(r"[^a-z0-9\s]", " ", s.lower()).strip()


# Prepare preprocessed maps
disease_symptoms_norm = {}   # disease -> list of normalized symptom phrases
disease_symptom_tokens = {}  # disease -> set of tokens across all its symptom phrases
disease_aliases_norm = {}    # disease -> list of normalized aliases

for disease, info in DISEASE_DB.items():
    sym_list = info.get("symptoms", []) or []
    norm_sym = [normalize_text(s) for s in sym_list if s and isinstance(s, str)]
    disease_symptoms_norm[disease] = norm_sym
    # combine tokens across symptoms
    tokens = set()
    for p in norm_sym:
        tokens.update([t for t in p.split() if t])
    disease_symptom_tokens[disease] = tokens

    aliases = info.get("aliases", []) or []
    disease_aliases_norm[disease] = [normalize_text(a) for a in aliases if a and isinstance(a, str)]
    # also include disease name itself as alias
    disease_aliases_norm[disease].append(normalize_text(disease))


def compute_confidence(user_text: str, disease: str) -> float:
    """
    Compute confidence [0..1] that `disease` matches `user_text`.
    Combines:
      - phrase overlap (exact phrase matches of symptom phrases) (weight 0.7)
      - token-level Jaccard (weight 0.2)
      - alias mention boost (weight 0.1)
    Also uses fuzzy token matches to give partial credit.
    """
    user_norm = normalize_text(user_text)
    if not user_norm:
        return 0.0

    user_tokens = set([t for t in user_norm.split() if t])

    symptoms = disease_symptoms_norm.get(disease, [])
    if not symptoms:
        return 0.0

    # Exact phrase matches
    phrase_matches = 0.0
    fuzzy_matches = 0.0
    for sym in symptoms:
        if not sym:
            continue
        # exact phrase match
        if re.search(r"\b" + re.escape(sym) + r"\b", user_norm):
            phrase_matches += 1.0
        else:
            # fuzzy: check if any token in symptom has a close match in user tokens
            sym_tokens = [t for t in sym.split() if t]
            for st in sym_tokens:
                close = get_close_matches(st, list(user_tokens), n=1, cutoff=0.85)
                if close:
                    fuzzy_matches += 0.5  # partial credit for fuzzy token match
                    break

    phrase_score = min(1.0, (phrase_matches + fuzzy_matches) / max(1, len(symptoms)))

    # token-level jaccard between user tokens and disease tokens
    disease_tokens = disease_symptom_tokens.get(disease, set())
    union = user_tokens.union(disease_tokens)
    inter = user_tokens.intersection(disease_tokens)
    token_jaccard = len(inter) / len(union) if union else 0.0

    # alias boost (if user mentions disease or alias)
    alias_hit = 0.0
    for alias in disease_aliases_norm.get(disease, []):
        if alias and re.search(r"\b" + re.escape(alias) + r"\b", user_norm):
            alias_hit = 1.0
            break

    # Combine with weights
    score = 0.7 * phrase_score + 0.2 * token_jaccard + 0.1 * alias_hit
    # Clip between 0 and 1
    return max(0.0, min(1.0, score))


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_input = (request.json.get("message", "") or "").strip()
        if not user_input:
            return jsonify({"reply": "Please enter your symptoms (e.g., fever, cough, headache)."}), 200

        # Compute confidence for every disease
        scores = []
        for disease in DISEASE_DB.keys():
            conf = compute_confidence(user_input, disease)
            scores.append((disease, conf))

        # Sort descending by confidence
        scores.sort(key=lambda x: x[1], reverse=True)

        # Gather top 3 non-zero results
        top_results = []
        for disease, conf in scores[:6]:  # look at top 6 then filter
            if conf <= 0.0:
                continue
            info = DISEASE_DB.get(disease, {})
            top_results.append({
                "disease": disease.title(),
                "aliases": ", ".join(info.get("aliases", [])),
                "symptoms": ", ".join(info.get("symptoms", [])),
                "medicines": info.get("medicines", ""),
                "precautions": info.get("precautions", ""),
                "specialist": info.get("specialist", ""),
                "confidence": f"{int(round(conf * 100))}%"
            })
            if len(top_results) >= 3:
                break

        # If top result not confident enough, do web-search fallback
        if not top_results or (top_results and int(top_results[0]["confidence"].strip("%")) < 25):
            # Try web search for more information
            try:
                query = f"symptoms: {user_input}"
                search_results = []
                if google_search:
                    # Some googlesearch versions accept num_results, others num/stop — try both
                    try:
                        search_results = list(google_search(query, num_results=4))
                    except TypeError:
                        # fallback older signature
                        search_results = list(google_search(query, num=4, stop=4))
                # Build web response if results found
                if search_results:
                    web_response = "I couldn't find a confident match in my database. Here are some web results that might help:<br>"
                    for url in search_results[:4]:
                        web_response += f'<a href="{url}" target="_blank" rel="noopener noreferrer">{url}</a><br>'
                    # Still include any weak DB suggestions (if present)
                    if top_results:
                        return jsonify({"results": top_results, "reply": web_response})
                    else:
                        return jsonify({"reply": web_response})
            except Exception as e:
                print("Web search failed:", e)
                traceback.print_exc()

        # If we do have top results, return them
        if top_results:
            return jsonify({"results": top_results})

        # final fallback
        return jsonify({"reply": "I couldn't confidently match those symptoms. Please consult a healthcare professional."})

    except Exception as e:
        print("Unexpected error:", e)
        traceback.print_exc()
        return jsonify({"reply": "Sorry — something went wrong while processing your request."})

if __name__ == "__main__":
    app.run(debug=True)
