from REPO import UsuarioREPO

class Usuario:
    racf = "" 
    nome = ""
    senha = ""
    email=""
    mudSenha = False
    nSessao = ""
    horarioSessao = ""

    def login(self, racf, senha):

        #verifica se o usuário esá com acesso. Se não estiver, retorna "-1"
        usuariorepo = UsuarioREPO()
        val, campos = usuariorepo.LoginREPO(racf, senha)
        if val == -1:
            return 404
        else:
            self.racf = campos['racf']
            self.nome = campos['nome']
            self.senha = campos['senha']
            self.email = campos['email']
            self.mudSenha = campos['precisaMudar']
            self.nSessao = campos['sessao']
            self.horarioSessao = campos['horaSess']
            #TODO -> Verificar se precisa mudar a senha e gerar tela para mudar a senha
            
            return 200

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
            
        


