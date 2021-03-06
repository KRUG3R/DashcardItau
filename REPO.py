import mysql.connector

class ParceiroREPO:
    def getResumoParceiroREPO(self):
        cnx = mysql.connector.connect(user='root', password='mysql',host='127.0.0.1',database='projetofinal')
        cursor = cnx.cursor()
        query = ("select id_agente, nome_agente from mtb310_ag_financeiro")
        cursor.execute(query)
        listaAgentes=[]
        for id_agente, nome_agente in cursor:
            registro = [id_agente, nome_agente]
            listaAgentes.append(registro)
        
        query = ("select nome_agente, volume_transacional from mtb310_ag_financeiro order by  volume_transacional desc limit 10")
        cursor.execute(query)

        listaTOP10 = []
        for nome_agente, volume_transacional in cursor:
            registro = {
               'Parceiro' : nome_agente,
               'Volume Transacional' : volume_transacional
            }
            listaTOP10.append(registro)
        cnx.close()
        return listaAgentes, listaTOP10



    def getDetalheParceiroREPO(self,ParceiroID):
        cnx = mysql.connector.connect(user='root', password='mysql',host='127.0.0.1',database='projetofinal')
        cursor = cnx.cursor()

        query = "select nome, volume, sum(sucesso) as sucesso, sum(falha) as falha, sum(fraude) as fraude "
        query +="from ( select AG.nome_agente as nome , AG.volume_transacional as volume , "
        query +="	IF(TR.status = 0 ,1,0) as sucesso , "
        query +="	IF(TR.status = 1,1,0) as falha, "
        query +="	IF(TR.status = 2,1,0) as fraude "
        query +="	from mtb310_ag_financeiro as AG "
        query +="	left join mtb310_transaction as TR "
        query +="	on TR.ag_financeiro = AG.id_agente "
        query +="	where AG.id_agente = " + ParceiroID
        query +=") as tab1 group by nome, volume"

        cursor.execute(query)
        dados = {}
        for nome, volume, sucesso, falha, fraude in cursor:
            dados = {
                'nome' : nome,
                'volume' : int(volume),
                'sucesso' : int(sucesso),
                'falha' : int(falha),
                'fraude' : int(fraude)
            }

        cnx.close()
        return dados



class UsuarioREPO:
    def ResetPasswordREPO(self, email):
        cnx = mysql.connector.connect(user='root', password='mysql',host='127.0.0.1',database='projetofinal')
        cursor = cnx.cursor()
        query = ("update usuario set senha = SHA1('senha123'), precisaMudar = True, horaSess=current_timestamp where email = '" + email + "'")
        print(query)
        cursor.execute(query)
        cnx.commit()
        retorno = cursor.rowcount
        print(retorno)
        cursor.close()
        cnx.close()
        return retorno
    
    def LoginREPO(self, racf, senha):
        cnx = mysql.connector.connect(user='root', password='mysql',host='127.0.0.1',database='projetofinal')
        cursor = cnx.cursor()
        # prmeiro atualiza dados d sessão:
        query = ("update usuario set sessao = MD5(concat(racf, current_timestamp)) , horaSess = current_timestamp where racf = '" + racf + "' and senha = SHA('" + senha + "')")
        cursor.execute(query)
        cnx.commit()

        # depois consulta com dados atualizados
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
        retorno = cursor.rowcount
        cursor.close()
        cnx.close()
        return retorno , saida
    
    def ValidaSessao(self, sessao):
        cnx = mysql.connector.connect(user='root', password='mysql',host='127.0.0.1',database='projetofinal')
        cursor = cnx.cursor()
        saida={}

        # valida se sessao está ativa.
        query = ("select racf from usuario where sessao = '" + sessao + "' and horaSess > ADDTIME(current_timestamp, '-20:0.000000');")
        cursor.execute(query)
        print(query)
        for r in cursor:
            print(r)

        valida = cursor.rowcount
        print(valida)

        if valida == 1:
            # Se sessão valida, update sessao:
            query = ("update usuario set horaSess = current_timestamp where sessao = '" + sessao + "'")
            cursor.execute(query)
            cnx.commit()

            #carrega dados de usuario para saída.
            query = ("select racf, nome, senha, email, precisaMudar, sessao, horaSess, urlFoto from usuario where sessao = '" + sessao + "'")
            cursor.execute(query)
            for racf, nome, senha, email, precisaMudar, Ssessao, horaSess, urlFoto in cursor:
                saida = {
                    'racf': racf,
                    'nome':nome,
                    'urlFoto':   urlFoto
                }
        return valida, saida
  