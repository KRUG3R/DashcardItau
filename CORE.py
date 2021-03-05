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
        #verifica se o usuário esá com acesso. Se não estiver, retorna "0"
        usuariorepo = UsuarioREPO()
        val, campos = usuariorepo.LoginREPO(racf, senha)
        if val == -1:
            return 404
        else:
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
            
        


