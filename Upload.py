from SeuModulo import app
from SeuModulo import log
import os
import uuid

class Upload(object):

    __imagens = ['.png','.jpg', '.jpeg', '.gif', '.bmp']
    __documentos = ['.doc','.docx', '.pdf', '.txt', '.xls', '.ppt']
    __audios = ['.mp3', '.ogg', '.wma', '.aac','.ac3', '.wav']
    __videos = ['.mp4', '.avi', '.mpeg', '.mov', '.rmvb', '.mkv', '.wmv']
    __comprimidos = ['.zip', '.rar', '.7z'] 
    
    # File e um objeto request.files do flask
    def __init__(self, file):
        self.__file = file
        self.__extensao = os.path.splitext(self.__file.filename)[-1].lower()
        self.__nome = str(uuid.uuid4()) + self.__extensao
        self.__path = ''
        self.__erro = ''
       
    def __valida(self):
        return '.' in self.__file.filename and \
            self.__file.filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

    def __caminho(self):
        pasta = app.config['UPLOAD_FOLDER']
        if self.__extensao in self.__imagens:
            pasta += '\\imagens'
        elif self.__extensao in self.__documentos:
            pasta += '\\documentos'
        elif self.__extensao in self.__audios:
            pasta += '\\audios'
        elif self.__extensao in self.__videos:
            pasta += '\\videos'
        elif self.__extensao in self.__comprimidos:
            pasta += '\\comprimidos'

        return pasta

    @property
    def path(self):
        return self.__path

    @property
    def erro(self):
        return self.__erro

    def salvar(self):
        self.__erro = 'Falha ao salvar arquivo.'
        try:
            upload = self.__caminho()
            if not self.__file.filename == '':
                if self.__file and self.__valida():
                    if not os.path.exists(upload):
                        try:
                            os.makedirs(upload)
                            self.__file.save(os.path.join(upload, self.__nome))
                            self.__path = upload + self.__nome
                            self.__erro = ''
                            return True
                        except:
                            log.logging()
                            self.__erro = 'Falha ao criar diretório'
                else:
                    self.__erro = 'Arquivo não suportado'
            else:
                self.__erro = 'Nenhum arquivo foi enviado.'
        except:
            log.logging()
        return False
