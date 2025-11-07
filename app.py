from flask import Flask, request, send_file, jsonify
from rembg import remove
from io import BytesIO
from PIL import Image

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"status": "✅ Rembg AI server is running!"})

@app.route('/remove', methods=['POST'])
def remove_bg():
    if 'image' not in request.files:
        return jsonify({"error": "يرجى إرسال صورة"}), 400

    image_file = request.files['image']
    try:
        input_image = Image.open(image_file.stream)
        output = remove(input_image)
        output_io = BytesIO()
        output.save(output_io, format='PNG')
        output_io.seek(0)
        return send_file(output_io, mimetype='image/png')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)