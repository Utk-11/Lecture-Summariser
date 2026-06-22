import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai

app = Flask(__name__)
CORS(app)

@app.route("/process_audio", methods=["POST"])
def handle_audio():
    if "audio" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
        
    file = request.files["audio"]
    target_lang = request.form.get("language", "Hindi")
    
    if file.filename == "":
        return jsonify({"error": "Filename is empty"}), 400

    # Save locally to send to the API
    temp_name = f"temp_{file.filename}"
    file.save(temp_name)

    try:
        client = genai.Client()
        upload = client.files.upload(file=temp_name)
        
        prompt = f"""
        You are an elite university engineering professor and technical translator.
        Analyze this class lecture recording carefully. 
        
        Provide your entire analysis completely written in the {target_lang} language. 
        Do not write an English version first—the user wants the final notes natively in {target_lang}.
        
        Structure your response with these exact points:
        1. Summary of Core Technical Concepts (summarized cleanly in {target_lang}).
        2. Key Terms and Formulas (Keep formulas in mathematical text format, but explain the definitions in {target_lang}).
        """
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[upload, prompt]
        )
        
        client.files.delete(name=upload.name)
        
        formatted_html = response.text.replace("\n", "<br>")
        return jsonify({"analysis": formatted_html})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
    finally:
        if os.path.exists(temp_name):
            os.remove(temp_name)

if __name__ == "__main__":
    app.run(port=5001)