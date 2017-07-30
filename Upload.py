from seuprojeto import app
import os
import uuid

class Upload(object):

    __imagens = ['.png','.jpg', '.jpeg', '.gif', '.bmp']
    __documentos = ['.doc','.docx', '.pdf', '.txt', '.xls', '.ppt']
    __audios = ['.mp3', '.ogg', '.wma', '.aac','.ac3', '.wav']
    __videos = ['.mp4', '.avi', '.mpeg', '.mov', '.rmvb', '.mkv', '.wmv']
    __comprimidos = ['.zip', '.rar', '.7z'] 
    
    def __init__(self, file):
        self.file = file
        self.extensao = os.path.splitext(self.file.filename)[-1].lower()
        self.nome = str(uuid.uuid4()) + self.extensao
        self.__path = ''   
       
    def __valida(self):
        return '.' in self.file.filename and \
            self.file.filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

    def __caminho(self):
        pasta = app.config['UPLOAD_FOLDER']
        if self.extensao in self.__imagens:
            pasta += '\\imagens'
        elif self.extensao in self.__documentos:
            pasta += '\\documentos'
        elif self.extensao in self.__audios:
            pasta += '\\audios'
        elif self.extensao in self.__videos:
            pasta += '\\videos'
        elif self.extensao in self.__comprimidos:
            pasta += '\\comprimidos'

        return pasta

    @property
    def path(self):
        return self.__path

    def salvar(self):
        upload = self.__caminho()
        if not self.file.filename == '':
            if self.file and self.__valida():
                if not os.path.exists(upload):
                    os.makedirs(upload)
                self.file.save(os.path.join(upload, self.nome))
                self.__path = upload + self.nome
                return True
        return False
