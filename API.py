import http.server
import socketserver
from CORE import Usuario
from CORE import Parceiros
from urllib.parse import urlparse
from urllib.parse import parse_qs

#EFETUA LOGIN --------------------------------------------------------------------------------
def do_login(self):
    length = int(self.headers["Content-Length"])
    corpoSTR = str(self.rfile.read(length),"utf-8")
    #print("corpoSTR:" + corpoSTR)
    campos = corpoSTR.split("&")
    campoValor=[]
    for i  in campos:
        rc = i.split("=")
        campoValor.append(rc)
    #print (campoValor)
    user = ""
    passwrd = ""
    for campo, valor in campoValor:
        if campo == "nome":
            user = valor
        if campo =="senha":
            passwrd = valor
    
    usuario = Usuario()
    retorno , sessao = usuario.login(user, passwrd)
    if retorno == 200:
        self.send_response(301)
        self.send_header('Location', 'AgentesFinanceiros.html?sessionCode=' + sessao)
        self.end_headers()
    else:
        html = f"<html><head></head><body><h1><red>Não OK!!!!!!!!!!</red></h1></body></html>"
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(html, "utf8"))
  
#BUSCA CONSOLIDADO PARCEIROS ------------------------------------------------------------------
def do_Parceiros(self):
    sessao = ''
    usuario = Usuario()
    query_components = parse_qs(urlparse(self.path).query)
    
    # Verifica se sessão é válida, se for reseta o tempo da sessao
    if 'sessionCode' in query_components:
        sessao = query_components['sessionCode'][0]

    if sessao != '':
        valida, campos = usuario.ValidaSessao(sessao)
    else:
        valida = 400
        campos = {}
    
    # Se Validou sessão, Consulta informação de parceiros
    if valida == 200:
        parceiro = Parceiros()
        listaAgentes, listaTOP10  = parceiro.getResumoParceiros()

        saida ={
            'usuario': campos,
            'Agentes':listaAgentes,
            'Top10': listaTOP10
        }

        html = str(saida)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(html, "utf8"))

    else:
        html = f"<html><head></head><body>sessao expirada, faça login novamente </body></html>"
        self.send_response(valida)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(html, "utf8"))

#BUSCA DETALHE DO PARCEIROS--------------------------------
def do_ParceiroDetalhe(self):
    sessao = ''
    parceiroID = ''
    usuario = Usuario()

    query_components = parse_qs(urlparse(self.path).query)
    # Verifica se sessão é válida, se for reseta o tempo da sessao
    if 'sessionCode' in query_components:
        sessao = query_components['sessionCode'][0]
    if 'parceiroID' in query_components:
        parceiroID = query_components['parceiroID'][0]

    if sessao != '' :
        valida, campos = usuario.ValidaSessao(sessao)
    else:
        valida = 400
        campos = {}
    
    # Se Validou sessão, Consulta informação de parceiros
    if valida == 200:
        parceiro = Parceiros()
        dados  = parceiro.getDetalheParceiros(parceiroID)
        html = str(dados)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(html, "utf8"))

    else:
        html = f"<html><head></head><body>sessao expirada, faça login novamente </body></html>"
        self.send_response(valida)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(html, "utf8"))            
     
   
#REINICIA SENHA --------------------------------------------------------------------------------
def do_RessetPassword(self):
    usuario = Usuario()
    email = ''
    query_components = parse_qs(urlparse(self.path).query)
    #print(query_components)
    if 'email' in query_components:
        email = query_components['email'][0]
    rc=usuario.ResetPassword(email)

    if rc==200:
        html = f"<html><head></head><body>Senha de {email} ressetada para senha123<br> <a href=\"index.html\">Voltar para tela de login</a></h1></body></html>"
        self.send_response(200)
    else:
        html = f"<html><head></head><body>Email {email} não encontrado</body></html>"
        self.send_response(rc)

    self.send_header("Content-type", "text/html")
    self.end_headers()
   
    self.wfile.write(bytes(html, "utf8"))
    return

#API ROUTER --------------------------------------------------------------------------------
class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/':
            self.path = 'index.html'
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
        elif self.path.find('/RessetPassword') == 0:
            do_RessetPassword(self)
        elif self.path.find('/parceiros') == 0:
            do_Parceiros(self)
        elif self.path.find('/parceiroDetalhe') == 0:
            do_ParceiroDetalhe(self)
        else:
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
        return

    def do_POST(self):
        if self.path.find('/login') == 0:
            do_login(self)
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            mensagem = 'Desculpe, Não Encontrado.'
            html = f"<html><head></head><body><h1>{mensagem}!</h1></body></html>"
            self.wfile.write(bytes(html, "utf8"))
        return

# Inicia Serviço na porta 8000 ----------------------------------------------------------
handler_object = MyHttpRequestHandler
PORT = 8000
my_server = socketserver.TCPServer(("", PORT), handler_object)
my_server.serve_forever()