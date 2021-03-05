import mysql.connector

class UsuarioREPO:
    def ResetPasswordREPO(self, email):
        cnx = mysql.connector.connect(user='root', password='mysql',host='127.0.0.1',database='projetofinal')
        cursor = cnx.cursor()
        query = ("update usuario set senha = SHA1('senha123'), precisaMudar = True where email = '" + email + "'")
        cursor.execute(query)
        cnx.commit()
        retorno = cursor.rowcount
        cursor.close()
        cnx.close()
        return retorno
    
    def LoginREPO(self, racf, senha):
        cnx = mysql.connector.connect(user='root', password='mysql',host='127.0.0.1',database='projetofinal')
        cursor = cnx.cursor()
        query = ("select racf, nome, senha, email, precisaMudar, sessao, horaSess from usuario where racf = '" + racf + "' and senha = SHA('" + senha + "')")
        cursor.execute(query)
        saida = {}
        for s_racf, s_nome, s_senha, s_email, s_precisaMudar, s_sessao, s_horaSess in cursor:
            saida = {
                'racf':s_racf, 
                'nome': s_nome,
                'senha': s_senha,
                'email': s_email, 
                'precisaMudar': s_precisaMudar,
                'sessao': s_sessao, 
                'horaSess':s_horaSess
            }
        #print("retorno login2:" + str(cursor.rowcount))
        #print("saida:"+  str(saida))
        retorno = cursor.rowcount
        cursor.close()
        cnx.close()
        return retorno , saida