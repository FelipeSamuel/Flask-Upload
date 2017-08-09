from seumodulo import app
from seumodulo import log
from flask import request
import os
import uuid
from hurry.filesize import size

class Upload(object):

    __imagens = ['.png','.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.bpg', '.ico', '.img', '.jps']
    __documentos = ['.doc','.docx', '.pdf', '.txt', '.xls', '.ppt', '.odp', '.pot', '.pps', '.csv']
    __audios = ['.mp3', '.ogg', '.wma', '.aac','.ac3', '.wav', '.aa', '.aac', '.aiff']
    __videos = ['.mp4', '.avi', '.mpeg', '.mov', '.rmvb', '.mkv', '.wmv', '.webm', '.flv', '.vob', '.mpg', '.m4v', '.3gp']
    __comprimidos = ['.zip', '.rar', '.7z', '.iso', '.tar', '.bz2', '.gz', '.dmg', '.tar.gz', '.tgz']
    __aplicativos = ['.exe', '.apk', '.deb', '.rpm', '.msi', '.jar', '.war', '.bin']
    __fontes = ['.ttf', '.ttc', '.woff', '.otf', '.tfm', '.otf']
    __vetores = ['.ai', '.cdr', '.cmx', '.eps', '.dxf', '.egt', '.svg', '.vsd']
    __photoshop = ['.psd']
    __scripts = ['.bat', '.cmd', '.js', '.php', '.py', '.vbs', '.cfg', '.conf']
    __estilos = ['.css', '.less', '.sass']
    __webpages = ['.html', '.htm', '.xhtml', '.mhtml', '.dtd', '.asp', '.jsp', '.phtml']
    __dados = ['.json', '.xml', '.db', '.eml', '.sql', '.bak', '.log']
    __temporarios = ['.temp', '.tmp']
    
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
        elif self.__extensao in self.__aplicativos:
            pasta += '\\aplicativos'
        elif self.__extensao in self.__fontes:
            pasta += '\\fontes'
        elif self.__extensao in self.__vetores:
            pasta += '\\vetores'
        elif self.__extensao in self.__scripts:
            pasta += '\\scripts'
        elif self.__extensao in self.__webpages:
            pasta += '\\webpages'
        elif self.__extensao in self.__dados:
            pasta += '\\dados'
        elif self.__extensao in self.__temporarios:
            pasta += '\\temporarios'
        elif self.__extensao in self.__photoshop:
            pasta += '\\photoshop'
        elif self.__extensao in self.__estilos:
            pasta += '\\estilos'

        return pasta


    @property
    def path(self):
        return self.__path

    @property
    def erro(self):
        return self.__erro

    @property
    def nome(self):
        return self.__nome

    @property
    def extensao(self):
        return self.__extensao

    @property
    def file(self):
        return self.__file

    def salvar(self):
        self.__erro = 'Falha ao salvar arquivo.'
        try:
            upload = self.__caminho()
            if not self.__file.filename == '':
                if self.__file and self.__valida():
                    if not os.path.exists(upload):
                        try:
                            os.makedirs(upload)
                        except:
                            log.logging()
                            self.__erro = 'Falha ao criar diretório.'
                    self.__file.save(os.path.join(upload, self.__nome))
                    self.__path = upload + self.__nome
                    self.__erro = ''
                    return True
                else:
                    self.__erro = 'Arquivo não suportado.'
            else:
                self.__erro = 'Nenhum arquivo foi enviado.'
        except:
            log.logging()
        return False


# Decorador
def file_upload(func):
        def uploading(*args, **kwargs):
            try:
                if request.method == 'POST':
                    retorno = None
                    caminhos = []
                    falhas = 0
                    sucesso = 0
                    total = 0
                    bytes_enviados = 0
                    for arquivo in request.files:
                        tamanho = request.files[arquivo].seek(0,2)
                        if request.files[arquivo]:
                            total += 1
                            if tamanho <= app.config['MAX_SIZE_UPLOAD']:
                                u = Upload(request.files[arquivo])
                                if u.salvar():
                                    caminhos.append(
                                        {
                                            "erro": False, 
                                            "campo": arquivo, 
                                            "caminho_completo": u.path,
                                            "extensao": u.extensao,
                                            "tamanho": size(tamanho),
                                            "nome_arquivo": u.nome,
                                            "msg": "Arquivo enviado com sucesso."
                                        })
                                    sucesso += 1
                                    bytes_enviados += tamanho
                                else:
                                    caminhos.append(
                                        {
                                            "erro": True, 
                                            "campo": arquivo, 
                                            "msg": u.erro
                                        })
                                    falhas +=1 
                            else:
                                caminhos.append(
                                            {
                                                "erro": True, 
                                                "campo": arquivo, 
                                                "msg": "O arquivo excede o tamanho máximo permitido."
                                            })
                                falhas +=1 

                    porcentagem_falhas =  round((100 * float(falhas) / float (total)), 2)
                    porcentagem_sucessos = round((100 * float(sucesso) / float (total)), 2)
                    retorno = {
                        "quantidade_falhas": falhas, 
                        "quantidade_sucessos": sucesso, 
                        "arquivos": caminhos,
                        "arquivos_enviados": total,
                        "bytes_enviados": size(bytes_enviados),
                        "porcentagem_de_falha": porcentagem_falhas,
                        "porcentagem_de_sucesso": porcentagem_sucessos,
                        "msg": str(porcentagem_sucessos)+'% dos arquivos foram enviados com sucesso.' if not caminhos == [] else "Os campos dos arquivos estão todos vazios."
                        }
                    return func(retorno, *args, **kwargs)
            except:
                log.logging()
            return func(*args, **kwargs)
        return uploading
