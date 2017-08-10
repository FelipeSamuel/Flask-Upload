from seumodulo import app
from seumodulo import log
from flask import request
from hurry.filesize import size
from hurry.filesize import alternative
import os
import uuid

class Upload(object):

    __imagens = ['.png','.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.bpg', '.ico', '.img', '.jps']
    __documentos = ['.doc','.docx', '.pdf', '.txt', '.xls', '.ppt', '.odp', '.pot', '.pps', '.csv', '.rtf']
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
            retorno = None
            try:
                if request.method == 'POST':
                    caminhos = []
                    quantidade_falhas = 0
                    quantidade_sucesso = 0
                    total = 0
                    bytes_enviados = 0
                    bytes_nao_enviados = 0
                    tamanho = 0
                    qtd = len(request.files)
                    if qtd > app.config['MAX_FILE_UPLOAD']:
                        retorno = {
                                "erro": True,
                                 "msg": "Quantidade máxima de arquivos excedida."
                                }
                    else:
                        for arquivo in request.files:
                            if request.files[arquivo]:
                                total += 1
                                tamanho = tamanho_arquivo(request.files[arquivo])
                                if tamanho <= app.config['MAX_SIZE_UPLOAD']:
                                    u = Upload(request.files[arquivo])
                                    if u.salvar():
                                        caminhos.append(
                                            {
                                                "erro": False, 
                                                "campo": arquivo, 
                                                "caminho_completo": u.path,
                                                "extensao": u.extensao,
                                                "tamanho": size(tamanho, system=alternative),
                                                "nome_arquivo": u.nome,
                                                "msg": "Arquivo enviado com sucesso."
                                            })
                                        quantidade_sucesso += 1
                                        bytes_enviados += tamanho
                                    else:
                                        caminhos.append(
                                            {
                                                "erro": True, 
                                                "tamanho": size(tamanho, system=alternative),
                                                "nome_arquivo": request.files[arquivo].filename,
                                                "campo": arquivo, 
                                                "msg": u.erro
                                            })
                                        bytes_nao_enviados = tamanho
                                        quantidade_falhas +=1 
                                else:
                                    caminhos.append(
                                                {
                                                    "erro": True, 
                                                    "campo": arquivo, 
                                                    "tamanho": size(tamanho, system=alternative),
                                                    "nome_arquivo": request.files[arquivo].filename,
                                                    "msg": "O arquivo excede o tamanho máximo permitido."
                                                })
                                    bytes_nao_enviados = tamanho
                                    quantidade_falhas +=1 

                        porcentagem_falhas = 0
                        porcentagem_sucessos = 0
                        if total != 0:
                            porcentagem_falhas =  round((100 * float(quantidade_falhas) / float (total)), 2)
                            porcentagem_sucessos = round((100 * float(quantidade_sucesso) / float (total)), 2)
                        retorno = {
                            "quantidade_falhas": quantidade_falhas, 
                            "quantidade_sucessos": quantidade_sucesso, 
                            "arquivos": caminhos,
                            "arquivos_enviados": total,
                            "bytes_enviados": size(bytes_enviados, system=alternative),
                            "bytes_nao_enviados": size(bytes_nao_enviados, system = alternative),
                            "porcentagem_de_falha": porcentagem_falhas,
                            "porcentagem_de_sucesso": porcentagem_sucessos,
                            "tamanho_maximo_permitido": size(app.config['MAX_SIZE_UPLOAD'], system = alternative),
                            "quantidade_maxima_permitida": app.config['MAX_FILE_UPLOAD'],
                            "msg": str(porcentagem_sucessos)+'% dos arquivos foram enviados com sucesso.' if not caminhos == [] else "Os campos dos arquivos estão todos vazios."
                            }
                    return func(retorno, *args, **kwargs)
            except:
                log.logging()
                retorno = {
                    "erro": True, 
                    "msg": "Falha ao realizar o upload dos arquivos."
                    }
            return func(retorno, *args, **kwargs)
        return uploading

# Decorador
def multi_file_upload(func):
        def uploading(*args, **kwargs):
            retorno = None
            try:
                if request.method == 'POST':
                    caminhos = []
                    quantidade_falhas = 0
                    quantidade_sucesso = 0
                    total = 0
                    bytes_enviados = 0
                    bytes_nao_enviados = 0
                    tamanho = 0
                    for up in request.files:
                        uploaded_files = request.files.getlist(up)
                        qtd = len(uploaded_files)
                        if qtd > app.config['MAX_FILE_UPLOAD']:
                            retorno = {
                                "erro": True,
                                "msg": "Quantidade máxima de arquivos excedida."
                                }
                        else:
                            for file in uploaded_files:
                                if file:
                                    total += 1
                                    tamanho = tamanho_arquivo(file)
                                    if tamanho <= app.config['MAX_SIZE_UPLOAD']:
                                        u = Upload(file)
                                        if u.salvar():
                                            caminhos.append(
                                                {
                                                    "erro": False, 
                                                    "campo": up, 
                                                    "caminho_completo": u.path,
                                                    "extensao": u.extensao,
                                                    "tamanho": size(tamanho, system=alternative),
                                                    "nome_arquivo": u.nome,
                                                    "msg": "Arquivo enviado com sucesso."
                                                })
                                            quantidade_sucesso += 1
                                            bytes_enviados += tamanho
                                        else:
                                            caminhos.append(
                                                {
                                                    "erro": True, 
                                                    "campo": up, 
                                                    "msg": u.erro,
                                                    "tamanho": size(tamanho, system=alternative),
                                                    "nome_arquivo": file.filename
                                                })
                                            bytes_nao_enviados = tamanho
                                            quantidade_falhas +=1 
                                    else:
                                        caminhos.append(
                                                    {
                                                        "erro": True, 
                                                        "campo": up, 
                                                        "tamanho": size(tamanho, system=alternative),
                                                        "nome_arquivo": file.filename,
                                                        "msg": "O arquivo excede o tamanho máximo permitido."
                                                    })
                                        bytes_nao_enviados = tamanho
                                        quantidade_falhas +=1 

                            porcentagem_falhas = 0
                            porcentagem_sucessos = 0
                            if total != 0:
                                porcentagem_falhas =  round((100 * float(quantidade_falhas) / float (total)), 2)
                                porcentagem_sucessos = round((100 * float(quantidade_sucesso) / float (total)), 2)
                            retorno = {
                                "quantidade_falhas": quantidade_falhas, 
                                "quantidade_sucessos": quantidade_sucesso, 
                                "arquivos": caminhos,
                                "arquivos_enviados": total,
                                "bytes_enviados": size(bytes_enviados, system=alternative),
                                "bytes_nao_enviados": size(bytes_nao_enviados, system=alternative),
                                "porcentagem_de_falha": porcentagem_falhas,
                                "porcentagem_de_sucesso": porcentagem_sucessos,
                                "tamanho_maximo_permitido": size(app.config['MAX_SIZE_UPLOAD'], system = alternative),
                                "quantidade_maxima_permitida": app.config['MAX_FILE_UPLOAD'],
                                "msg": str(porcentagem_sucessos)+'% dos arquivos foram enviados com sucesso.' if not caminhos == [] else "Os campos dos arquivos estão todos vazios."
                                }
                    return func(retorno, *args, **kwargs)
            except:
                log.logging()
                retorno = {
                    "erro": True, 
                    "msg": "Falha ao realizar o upload dos arquivos."
                    }
            return func(retorno, *args, **kwargs)
        return uploading

# Retorna o tamnanho de um arquivo 
def tamanho_arquivo(fobj):
    if fobj.content_length:
        return fobj.content_length
    try:
        pos = fobj.tell()
        fobj.seek(0, 2)
        size = fobj.tell()
        fobj.seek(pos)
        return size
    except (AttributeError, IOError):
        log.logging()
        pass
    return 0
