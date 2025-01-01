from flask import Flask, render_template, request, jsonify, send_file
from flask_socketio import SocketIO, emit
import yt_dlp
import os

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form.get('video_url')
    if not video_url:
        return jsonify({"error": "Por favor, ingresa un enlace de video."}), 400

    try:
        def progress_hook(d):
            if d['status'] == 'downloading':
                percent = d['_percent_str'].strip('%')
                socketio.emit('progress', {'percent': percent}, namespace='/download')

        ydl_opts = {
            'outtmpl': 'temp_video.%(ext)s',
            'format': 'best',
            'progress_hooks': [progress_hook],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            file_path = ydl.prepare_filename(info)

        return send_file(file_path, as_attachment=True, download_name=os.path.basename(file_path))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

if __name__ == '__main__':
    socketio.run(app, debug=True)
