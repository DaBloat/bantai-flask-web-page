from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime
from transformers import AutoTokenizer
import os

app = Flask(__name__)
LLM_MODEL = "HuggingFaceH4/zephyr-7b-beta"

UPLOAD_FOLDER = os.path.join('static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

HF_API_URL = f"https://api-inference.huggingface.co/models/{LLM_MODEL}"
# HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL)

@app.route('/',methods=['GET'])
def homepage():
    greet = {'AM':'Good Morning', 'PM':'Good Afternoon'}
    stats = {
        'greet': greet[datetime.now().strftime("%p")],
        'user': 'Admin',
        'customers': 10,
        'customer_trend': 'up',
        'violations': 5,
        'violation_trend': 'down'
    }
    return render_template('index.html', stat=stats)

@app.route('/chat',methods=["POST"])
def chat():
    # chat due to token restrains
    return jsonify({"reply": 'Pops to the Mighty Goods'})

@app.route("/content/<section>")
def choose_vid(section):
    global CURRENT_SECTION
    CURRENT_SECTION = section
    see = [i for i in os.listdir(UPLOAD_FOLDER)]
    if section == 'worker':
        if 'video_worker.mp4' in see:
            return f"""
                    <video class='cctv' loop autoplay width="100%" height="100%">
                        <source class='cctv' src="{os.path.join(UPLOAD_FOLDER, 'video_worker.mp4')}" type="video/mp4">
                        Your browser does not support the video tag.
                    </video>
                   """
        else:
            return """
                    <div class="upload-area">
                        <label for="video-upload">Connect Worker's CCTV</label>
                        <input type="file" id="video-upload" accept="video/*" />
                    </div>
                """
    elif section == 'customer':
        if 'video_customer.mp4' in see:
            return f"""
                    <video class='cctv' loop autoplay width="100%" height="100%">
                        <source class='cctv' src="{os.path.join(UPLOAD_FOLDER, 'video_customer.mp4')}" type="video/mp4">
                        Your browser does not support the video tag.
                    </video>
                   """
        else:
            return """
                    <div class="upload-area">
                        <label for="video-upload">Connect Customer's CCTV</label>
                        <input type="file" id="video-upload" accept="video/*" />
                    </div>
                """
    elif section == 'none':
        return """"""
    return "<h3>No Content Found</h3>", 404


@app.route('/upload-video', methods=['POST'])
def upload_video():
    file = request.files.get('video')
    if not file:
        return "No video uploaded", 400

    filename = f"video_{CURRENT_SECTION}.mp4"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    video_url = f"/static/uploads/{filename}"
    # Return HTML to display the video
    return f"""
        <video class='cctv' loop autoplay width="100%" height="100%">
            <source class='cctv' src="{video_url}" type="video/mp4">
            Your browser does not support the video tag.
        </video>
    """

if __name__ == '__main__':
    app.run(debug=True)
