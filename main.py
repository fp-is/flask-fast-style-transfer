from flask import Flask, request, render_template
from flask_cors import CORS, cross_origin
from style_transfer import process
from werkzeug.utils import secure_filename
from PIL import Image
from resizeimage import resizeimage
import os
import json

UPLOAD_FOLDER = os.getcwd() + '/static/in'

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
app.config['CORS_HEADER'] = 'Content-Type'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/api/convert', methods=['POST'])
def convert():
    image = request.files['image']
    style = request.form['style']
    filename = secure_filename(image.filename)
    image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    fd_img = open(UPLOAD_FOLDER+'/'+filename, 'rb+')
    image = Image.open(fd_img)
    image = resizeimage.resize_thumbnail(image, [512, 512])
    image.save(
        os.path.join(app.config['UPLOAD_FOLDER'], filename),
        image.format
    )
    fd_img.close()
    process(UPLOAD_FOLDER+'/'+filename, style)
    style = os.path.basename(style)
    content = dict(
        statusCode=200,
        before='/static/in/'+filename,
        after='/static/out/'+style+'-'+filename
    )
    return json.dumps(content)


@app.route('/api/ping', methods=['GET'])
def ping():
    content = dict(statusCode=200, body={'content': 'PONG'})
    return json.dumps(content)


@app.route('/')
@cross_origin()
def render_static():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
