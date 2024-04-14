from flask import Flask, request, jsonify
import pytesseract
from PIL import Image

app = Flask(__name__)

@app.route('/', methods=['POST'])
def extract_text():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'})

    image_file = request.files['image']

    if image_file.filename == '':
        return jsonify({'error': 'No image filename provided'})

    image = Image.open(image_file)
    custom_oem_psm_config = r'--oem 3 --psm 1'
    custom_lang = 'eng'
    extracted_text = pytesseract.image_to_string(image, config = custom_oem_psm_config, lang = custom_lang)
    return jsonify({'message': extracted_text})

if __name__ == '__main__':
    app.run(debug=True)
