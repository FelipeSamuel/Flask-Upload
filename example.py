from flask import Flask
from flask import request
from flask import jsonify
from Upload import file_upload, multi_file_upload
import os

app = Flask(__name__)

# Config Uploads
app.config['APP_DIR'] =  os.path.abspath(__file__)+"\\.."
app.config['UPLOAD_FOLDER'] = app.config['APP_DIR']+'\\uploads'
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg'])
app.config['MAX_FILE_UPLOAD'] = 4
app.config['MAX_SIZE_UPLOAD'] = 10000 # em bytes

"""
Usados Para inputs simples
Pode ser criado um formulario com diversos campos desse tipo
Porem so sera enviado com a anotacao @file_upload
Deve ser configurado a quantidade máxima de arquivos de upload. app.config['MAX_FILE_UPLOAD']
Deve ser configurado o tamanho máxim do arquivo para upload. app.config['MAX_SIZE_UPLOAD']
"""
@app.route('/upload', methods=['POST', 'GET'])
@file_upload
def upload(resultado):
  if request.method == 'GET':
    return '''
    <form action="/api/upload" method="post" enctype="multipart/form-data">

          <input type="file" name="file"/> </br>
          <input type="file" name="file2" /> </br>

          <input type="submit" value="Upload" />
     </form>
     '''
  # Retorna um discionario
  return jsonify(resultado)


"""
Usados para inputs com a propriedade "multiple"
Pode ser criado um formulario com diversos campos desse tipo
Porem, so sera enviado com a anotacao @multi_file_upload
Deve ser configurado a quantidade máxima de arquivos de upload. app.config['MAX_FILE_UPLOAD']
Deve ser configurado o tamanho máxim do arquivo para upload. app.config['MAX_SIZE_UPLOAD']
"""
@app.route('/upload/multiplo', methods=['POST', 'GET'])
@multi_file_upload
def multi_upload(resultado = ''):
  if request.method == 'GET':
    return '''
    <form action="/api/upload" method="post" enctype="multipart/form-data">

          <input type="file" name="file[]" multiple/> </br>
          <input type="file" name="file2[]" multiple /> </br>

          <input type="submit" value="Upload" />
     </form>
     '''
  # Retorna um discionario
  return jsonify(resultado)
        
if __name__ == '__main__':
  app.run(port=8080, debug=True)
