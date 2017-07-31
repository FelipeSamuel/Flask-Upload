from flask import Flask
from flask import request
from flask import jsonify
from Upload import Upload
from Upload import file_upload
import os

app = Flask(__name__)

# Config Uploads
app.config['APP_DIR'] =  os.path.abspath(__file__)+"\\.."
app.config['UPLOAD_FOLDER'] = app.config['APP_DIR']+'\\uploads'
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg'])

@app.route('/')
def index():
  return render_template('upload.html')
  
@app.route('/upload', methods=['POST'])
@file_upload
def upload(resultado):
  return jsonify(resultado)
        
if __name__ == '__main__':
  app.run(port=8080, debug=True)
