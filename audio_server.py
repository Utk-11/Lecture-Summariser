import os
from flask import Flask, request, jsonify
from flask_cors import CORS  # type: ignore
from google import genai
import tempfile

app = Flask(__name__)
# allow cors for live server port
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500"}})

@app.route("/process_audio", methods=["POST"])
def handle_audio():
    print("Received a request...")
    
    if "audio" not in request.files:
        print("Error: No audio file found in request")
        return jsonify({"error": "No file uploaded"}), 400
        
    file = request.files["audio"]
    target_lang = request.form.get("language", "Hindi")
    
    if file.filename == "":
        print("Error: Blank filename")
        return jsonify({"error": "Filename is empty"}), 400

    # saving to mac system temp folder so live server stops refreshing the page
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, f"temp_{file.filename}")
    file.save(temp_path)
    print(f"Saved file locally to: {temp_path}")

    try:
        # gemini api setup
        client = genai.Client()
        print("Uploading file to gemini...")
        audio_upload = client.files.upload(file=temp_path)
        
        prompt = f"""
        You are an elite university engineering professor and technical translator.
        Analyze this class lecture recording carefully. 
        
        Provide your entire analysis completely written in the {target_lang} language. 
        Do not write an English version first—the user wants the final notes natively in {target_lang}.
        
        Structure your response with these exact points:
        1. Summary of Core Technical Concepts (summarized cleanly in {target_lang}).
        2. Key Terms and Formulas (Keep formulas in mathematical text format, but explain the definitions in {target_lang}).
        """
        
        print("Generating notes from model...")
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[audio_upload, prompt]
        )
        
        # delete from cloud storage
        client.files.delete(name=audio_upload.name)
        print("Deleted cloud file.")
        
        # return clean markdown back to marked.js
        return jsonify({"analysis": response.text})
        
    except Exception as e:
        print(f"Something went wrong: {str(e)}")
        return jsonify({"error": str(e)}), 500
        
    finally:
        # clean up the temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)
            print("Cleaned up local temp file.")

if __name__ == "__main__":
    # running on port 5001
    app.run(port=5001, debug=True)