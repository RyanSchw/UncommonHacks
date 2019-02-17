from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit
import sys
sys.path.append("..")

from VideoProcess import VideoProcess
from Sample import Sample
from Lap import Checkpoint, Run

import os

app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = 'uploads'
socketio = SocketIO(app)
#p = VideoProcess(video_path="../phone_app/uploads/video.webm", debug=False)
p = VideoProcess(video_path="../resources/car_test_2_motion.webm", debug=False)

parsed_path = []


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
    global parsed_path

    parsed_path = p.process_video()
    out = Sample.serialize_array(parsed_path)
    with app.app_context():
        socketio.emit('data_vis', {'data': out}, broadcast=True, namespace='/sock')

    return '200'

@socketio.on('req-rec', namespace='/sock')
def test_message(message):
    print(message)
    emit('record', {'data': message}, broadcast=True)

@socketio.on('connect', namespace='/sock')
def test_connect():
    emit('hello', {'data': True})

@socketio.on('get_checkpoints', namespace='/sock')
def get_checkpoints(message):
    print(message['data'])
    itr = Checkpoint.deserialize_array(message['data'])
    checkpoints = []
    global parsed_path
    for i, indv in enumerate(itr):
        node1, node2 = Checkpoint.deserialize(indv)
        checkpoint = Checkpoint(i, node1, node2)
        checkpoints.append(checkpoint)
    run = Run(parsed_path, checkpoints).summary()
    print(run)

    emit('summary', {'data':run}, broadcast=True)

if __name__ == "__main__":
    app.run(ssl_context=('cert.pem', 'key.pem'), host ="0.0.0.0")
