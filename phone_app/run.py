from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit
import sys
sys.path.append("..")

from VideoProcess import VideoProcess

import os

app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = 'uploads'
socketio = SocketIO(app)
p = VideoProcess(video_path="../phone_app/uploads/video.webm", debug=False)


@app.route('/', methods=['GET'])
def ui():
    return app.send_static_file('ui.html')

@app.route('/js/<path:path>')
def send_js(path):
    return app.send_static_file('js/' + path)

@app.route('/record', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/save-file', methods=['POST'])
def save_record():
    print(request.files['file'].filename) 
    file = request.files['file']
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

    path = p.process_video()
    
    emit('data_vis', {'data': path})


    return '200'


@socketio.on('req-rec', namespace='/sock')
def test_message(message):
    print(message)
    emit('record', {'data': message}, broadcast=True)



@socketio.on('connect', namespace='/sock')
def test_connect():
    emit('hello', {'data': True})

if __name__ == "__main__":
    app.run(ssl_context=('cert.pem', 'key.pem'), host ="0.0.0.0")