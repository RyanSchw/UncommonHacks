from flask import Flask,  request, render_template
from flask_socketio import SocketIO, emit

import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
socketio = SocketIO(app)


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/save-file', methods=['POST'])
def save_record():
    print(request.files['file'].filename) 
    file = request.files['file']
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
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