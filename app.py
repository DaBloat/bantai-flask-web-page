from flask import Flask, render_template, request, jsonify
import requests
import cv2
from ultralytics import YOLO
from datetime import datetime
from transformers import AutoTokenizer
import os

app = Flask(__name__)
LLM_MODEL = "HuggingFaceH4/zephyr-7b-beta"
PEOPLE_CNT_MODEL = YOLO("people-counter.pt")
PPE_MODEL = YOLO("ppe.pt")

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
        if 'video_worker_boxes_q.mp4' in see:
            return f"""
                    <video class='cctv' loop autoplay width="100%" height="100%">
                        <source class='cctv' src="{os.path.join(UPLOAD_FOLDER, 'video_worker_boxes_q.mp4')}" type="video/mp4">
                        Your browser does not support the video tag.3
                    </video>
                   """
        else:
            return """
                    <div class="upload-area">
                        <label class='connect-cctv' for="video-upload">Connect Worker's CCTV</label>
                        <input type="file" id="video-upload" accept="video/*" />
                    </div>
                """
    elif section == 'customer':
        if 'video_customer_boxes_q.mp4' in see:
            return f"""
                    <video class='cctv' loop autoplay width="100%" height="100%">
                        <source class='cctv' src="{os.path.join(UPLOAD_FOLDER, 'video_customer_boxes_q.mp4')}" type="video/mp4">
                        Your browser does not support the video tag.
                    </video>
                   """
        else:
            return """
                    <div class="upload-area">
                        <label class='connect-cctv' for="video-upload">Connect Customer's CCTV</label>
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
    
    filename_block = f"video_{CURRENT_SECTION}_boxes.mp4"
    output_video_path = os.path.join(UPLOAD_FOLDER, filename_block)
    video_url = f"/static/uploads/{filename}"

    cap = cv2.VideoCapture(filepath)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    model = {'customer':PEOPLE_CNT_MODEL ,'worker':PPE_MODEL }

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Run YOLO prediction
        results = model[CURRENT_SECTION].predict(frame, imgsz=640, conf=0.25)

        # Draw boxes on the frame
        annotated_frame = results[0].plot()

        # Write the annotated frame to output video
        out.write(annotated_frame)

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    command = f'ffmpeg -i {output_video_path} -vcodec libx264 -acodec aac {os.path.join(UPLOAD_FOLDER, f"video_{CURRENT_SECTION}_boxes_q.mp4")}'
    os.system(command)
    video_url_block = f"/static/uploads/video_{CURRENT_SECTION}_boxes_q.mp4"

    # Return HTML to display the video
    return f"""
        <video class='cctv' loop autoplay width="100%" height="100%">
            <source class='cctv' src="{video_url_block}" type="video/mp4">
            Your browser does not support the video tag.
        </video>
    """

if __name__ == '__main__':
    app.run(debug=True)
