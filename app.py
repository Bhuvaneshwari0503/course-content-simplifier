"""
app.py
------
Flask application entry point for the Course Content Simplification Agent.
Defines all routes and connects the frontend with the Granite AI service.
"""

import sys
import traceback
from flask import Flask, render_template, request, jsonify

# Validate that credentials have been set before any request is processed
from config import PROJECT_ID, API_KEY, ENDPOINT_URL
from services.granite_service import simplify_content

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False


# ---------------------------------------------------------------------------
# Credential check on startup
# ---------------------------------------------------------------------------

def _check_credentials():
    issues = []

    if not PROJECT_ID:
        issues.append("PROJECT_ID")

    if not API_KEY:
        issues.append("API_KEY")

    if not ENDPOINT_URL:
        issues.append("ENDPOINT_URL")

    return issues


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    """Serve the main application page."""
    return render_template("index.html")


@app.route("/api/simplify", methods=["POST"])
def api_simplify():
    """
    POST /api/simplify
    Body (JSON): { "content": "...", "level": "beginner|intermediate|advanced|expert" }
    Response:    { "success": true, "data": { difficulty, complexity_level, concepts, simplified_text } }
    """
    try:
        body = request.get_json(force=True, silent=True)
        if not body:
            return jsonify({"success": False, "error": "Request body must be JSON."}), 400

        content = body.get("content", "").strip()
        level = body.get("level", "").strip().lower()

        # Input validation
        if not content:
            return jsonify({"success": False, "error": "Please provide educational content to simplify."}), 400

        if len(content) > 8000:
            return jsonify({"success": False, "error": "Content is too long. Please limit input to 8000 characters."}), 400

        valid_levels = {"beginner", "intermediate", "advanced", "expert"}
        if level not in valid_levels:
            return jsonify({"success": False, "error": f"Invalid level. Choose from: {', '.join(sorted(valid_levels))}."}), 400

        # Check credentials before making a live API call
        # Check credentials before making a live API call
        if not PROJECT_ID or not API_KEY or not ENDPOINT_URL:
            return jsonify({
                "success": False,
                "error": "IBM credentials are not configured."
            }), 503

        # Call IBM Granite
        result = simplify_content(content, level)

        return jsonify({"success": True, "data": result})

    except ValueError as ve:
        return jsonify({"success": False, "error": str(ve)}), 400

    except Exception as exc:
        # Log full traceback to console for debugging; return safe message to client
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": f"An error occurred while contacting IBM Watsonx.ai: {str(exc)}"
        }), 500


@app.route("/api/health", methods=["GET"])
def health():
    """Simple health-check endpoint."""
    configured = bool(
        PROJECT_ID and
        API_KEY and
        ENDPOINT_URL
    )
    return jsonify({
        "status": "ok",
        "credentials_configured": configured
    })


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("\n🎓 Course Content Simplification Agent")
    print("   Powered by Watsonx.ai\n")
    app.run(debug=True)
