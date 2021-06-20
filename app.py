import requests,uuid
import matplotlib.image as mpimg

from flask import Flask, flash, request, redirect, url_for, render_template
# import urllib.request
import os
from azure.storage.blob import BlobClient

from werkzeug.utils import secure_filename

app = Flask(__name__)


#UPLOAD_FOLDER = 'static/uploads/'

app.secret_key = "secret key"
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png','jpg'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        blobname = str(uuid.uuid4()) + ".jpg"

       # blob = BlobClient.from_connection_string(
            #conn_str="DefaultEndpointsProtocol=https;AccountName=imageclassification1;AccountKey=R0X33tP9FY0TfKwZ+O2BznpwDUZZWxbF2lJE3ToLhF4Dox/2V+frwVYUmEq3yDXAg+M5bszachzBpZDfT05CDA==;EndpointSuffix=core.windows.net",
           # container_name="sampleimage", blob_name=blobname)
        #blob.upload_blob(file)
        #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print('upload_image filename: ' + filename)
        img = mpimg.imread(file)
        img = img / 255
        img = img.reshape(784)
        input_data = "{\"data\": [" + str(list(img)) + "]}"
        headers = {'Content-Type': 'application/json'}
        service = 'http://67950230-b801-4e95-a607-7f5dd49a5908.centralus.azurecontainer.io/score'
        resp = requests.post(service, input_data, headers=headers)
        m = resp.text
        # m = "sss"
        flash('The predicted number is: ' + m[1])
        return render_template('index.html')
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)


@app.route('/display/<filename>')
def display_image(filename):
    print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


