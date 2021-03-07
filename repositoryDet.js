
  function httpGetDados(session, parceiroID)
  {
      var xmlHttp = new XMLHttpRequest();
      var theUrl = 'http://localhost:8000/parceiroDetalhe?sessionCode='+session+'&parceiroID='+parceiroID
      xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
      xmlHttp.send( null );
      if(xmlHttp.status!=200){
        window.location.replace("http://localhost:8000/?msg=SessaoExpirada");
      }
      var dadosJson = JSON.parse(xmlHttp.responseText.replaceAll(/'/g,'"'));
      return dadosJson;
  }

  function getSession() {
    var url = new URL(window.location.href);
    var session = url.searchParams.get("sessionCode");
    return session;
  }
  function getParceiroID() {
    var url = new URL(window.location.href);
    var session = url.searchParams.get("parceiro");
    return session;
  }

  function atualizaDados() {
    document.getElementById("nome").textContent = nome; 
    document.getElementById("sucesso").textContent = sucesso; 
    document.getElementById("falhas").textContent = falha;
    document.getElementById("fraudes").textContent = fraude;
  }

let sessao = getSession();
let parceiroID = getParceiroID();
let dados = httpGetDados(sessao,parceiroID);

let nome = dados['nome'] + " / " + dados['volume'];
let sucesso = dados['sucesso']
let falha = dados['falha']
let fraude = dados['fraude']


atualizaDados(nome,sucesso,falha,fraude);




