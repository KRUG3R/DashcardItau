from REPO import UsuarioREPO
from REPO import ParceiroREPO

class Parceiros:
    def getResumoParceiros(self):
        print("getListaParceiros")
        parceiroREPO = ParceiroREPO()
        listaAgentes, listaTOP10 = parceiroREPO.getResumoParceiroREPO()
        return  listaAgentes, listaTOP10 

    def getDetalheParceiros(self,parceiro_id):
        print("getListaParceiros")
        parceiroREPO = ParceiroREPO()
        dados = parceiroREPO.getDetalheParceiroREPO(parceiro_id)
        return  dados


class Usuario:
    racf = "" 
    nome = ""
    senha = ""
    email=""
    mudSenha = False
    nSessao = ""
    horarioSessao = ""
    urlFoto = ""

    def login(self, racf, senha):

        #verifica se o usuário esá com acesso. Se não estiver, retorna "-1"
        usuariorepo = UsuarioREPO()
        val, campos = usuariorepo.LoginREPO(racf, senha)
        if val == -1:
            return 404 , ''
        else:
            self.racf = campos['racf']
            self.nome = campos['nome']
            self.senha = campos['senha']
            self.email = campos['email']
            self.mudSenha = campos['precisaMudar']
            self.nSessao = campos['sessao']
            self.horarioSessao = campos['horaSess']
            #TODO -> Verificar se precisa mudar a senha e gerar tela para mudar a senha
            
            return 200 , self.nSessao

    def ResetPassword(self, email):
        try:
            usuariorepo = UsuarioREPO()
            updt = usuariorepo.ResetPasswordREPO(email)
            if updt > 0:
                return 200
            else:
                return 404
        except:
            return 404
    
    def ValidaSessao(self, sessao):
        usuarioREPO = UsuarioREPO()
        valida, campos = usuarioREPO.ValidaSessao(sessao)
        if valida == 1:
            self.racf = campos['racf']
            self.nome = campos['nome']
            self.urlFoto = campos['urlFoto']
            return 200, campos
        else:
            return 400, campos

            
        


