import http.server
import socketserver
from CORE import Usuario
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
    retorno = usuario.login(user, passwrd)
    if retorno == 200:
        html = f"<html><head></head><body><h1>OK</h1></body></html>"
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(html, "utf8"))
    else:
        html = f"<html><head></head><body><h1><red>Não OK!!!!!!!!!!</red></h1></body></html>"
        self.send_response(200)
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