
'''from flask import Flask, request, render_template, send_from_directory
import os
import json

from model import run_target_speaker_extraction

# Whisper + Translator
from faster_whisper import WhisperModel
from deep_translator import GoogleTranslator

app = Flask(__name__)

# -----------------------
# Load Whisper once
# -----------------------
whisper_model = WhisperModel("small", device="cpu", compute_type="int8")

# -----------------------
# Routes
# -----------------------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload")
def upload_page():
    return render_template("temp.html")


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory("uploads", filename)


@app.route("/outputs/<filename>")
def output_file(filename):
    return send_from_directory("outputs", filename)


@app.route("/extract", methods=["POST"])
def extract():

    # -------------------------------
    # CASE 1: TRANSCRIPTION REQUEST
    # -------------------------------
    if "transcribe" in request.form:
        audio_path = request.form["enhanced_audio"]
        lang = request.form["language"]

        similarities = json.loads(request.form.get("similarities", "[]"))
        selected_source_path = request.form.get("selected_source_path")
        mixed_audio_path = request.form.get("mixed_audio_path")

        segments, _ = whisper_model.transcribe(audio_path)
        text = " ".join(seg.text for seg in segments)

        if lang == "telugu":
            text = GoogleTranslator(source="auto", target="te").translate(text)
        elif lang == "hindi":
            text = GoogleTranslator(source="auto", target="hi").translate(text)

        return render_template(
            "last.html",
            enhanced_audio_path=audio_path,
            mixed_audio_path=mixed_audio_path,
            similarities=similarities,
            selected_source_path=selected_source_path,
            transcription=text
        )

    # -------------------------------
    # CASE 2: TARGET SPEAKER EXTRACTION
    # -------------------------------
    try:
        os.makedirs("uploads", exist_ok=True)
        os.makedirs("outputs", exist_ok=True)

        mixed_file = request.files["mixed"]
        target_file = request.files["target"]

        mixed_path = os.path.join("uploads", "mixed.wav")
        target_path = os.path.join("uploads", "target.wav")

        mixed_file.save(mixed_path)
        target_file.save(target_path)

        result = run_target_speaker_extraction(
            mixed_audio_path=mixed_path,
            target_audio_path=target_path,
            out_folder="outputs"
        )

        return render_template(
            "last.html",
            mixed_audio_path="/uploads/mixed.wav",
            enhanced_audio_path="/outputs/" + os.path.basename(result["enhanced_output_path"]),
            selected_source_path=result["selected_source_path"],
            similarities=result["similarities"],
            transcription=None
        )

    except Exception as e:
        return render_template(
            "last.html",
            error=str(e),
            mixed_audio_path="",
            enhanced_audio_path="",
            similarities=[]
        )


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)'''
from flask import Flask, request, render_template, send_from_directory
import os
import json

from model import run_target_speaker_extraction

# Whisper + Translator
from faster_whisper import WhisperModel
from deep_translator import GoogleTranslator

app = Flask(__name__)

# -----------------------
# Load Whisper ONCE
# -----------------------
whisper_model = WhisperModel("small", device="cpu", compute_type="int8")


# -----------------------
# Routes
# -----------------------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload")
def upload_page():
    return render_template("temp.html")


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory("uploads", filename)


@app.route("/outputs/<filename>")
def output_file(filename):
    return send_from_directory("outputs", filename)


@app.route("/extract", methods=["POST"])
def extract():

    # =====================================================
    # 🎤 CASE 1 — TRANSCRIPTION REQUEST (FIXED)
    # =====================================================
    if "transcribe" in request.form:

        # URL path from HTML (e.g. /outputs/enhanced_target.wav)
        audio_url = request.form["enhanced_audio"]

        # 🔑 FIX: Convert URL path → local file path
        audio_path = audio_url.lstrip("/") if audio_url.startswith("/") else audio_url

        print("🎧 Transcribing:", audio_path)
        print("📁 File exists:", os.path.exists(audio_path))

        lang = request.form["language"]

        similarities = json.loads(request.form.get("similarities", "[]"))
        selected_source_path = request.form.get("selected_source_path")
        mixed_audio_path = request.form.get("mixed_audio_path")

        # 🔊 Whisper transcription
        segments, _ = whisper_model.transcribe(
            audio_path,
            beam_size=5
        )

        text = " ".join(seg.text for seg in segments)

        # 🌐 Translation
        if lang == "telugu":
            text = GoogleTranslator(source="auto", target="te").translate(text)
        elif lang == "hindi":
            text = GoogleTranslator(source="auto", target="hi").translate(text)

        return render_template(
            "last.html",
            enhanced_audio_path=audio_url,
            mixed_audio_path=mixed_audio_path,
            similarities=similarities,
            selected_source_path=selected_source_path,
            transcription=text
        )

    # =====================================================
    # 🎛 CASE 2 — TARGET SPEAKER EXTRACTION PIPELINE
    # =====================================================
    try:
        os.makedirs("uploads", exist_ok=True)
        os.makedirs("outputs", exist_ok=True)

        mixed_file = request.files["mixed"]
        target_file = request.files["target"]

        mixed_path = os.path.join("uploads", "mixed.wav")
        target_path = os.path.join("uploads", "target.wav")

        mixed_file.save(mixed_path)
        target_file.save(target_path)

        result = run_target_speaker_extraction(
            mixed_audio_path=mixed_path,
            target_audio_path=target_path,
            out_folder="outputs"
        )

        return render_template(
            "last.html",
            mixed_audio_path="/uploads/mixed.wav",
            enhanced_audio_path="/outputs/" + os.path.basename(result["enhanced_output_path"]),
            selected_source_path=result["selected_source_path"],
            similarities=result["similarities"],
            transcription=None
        )

    except Exception as e:
        return render_template(
            "last.html",
            error=str(e),
            mixed_audio_path="",
            enhanced_audio_path="",
            similarities=[]
        )


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)


