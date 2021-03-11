function getSession(){
    var strUser = localStorage.getItem("userDASH");
    if (!strUser){    // se o objeto não existe no localStorage, signifca que eu não estou conectado
      window.location = "index.html";
      return;
    }
    var user = JSON.parse(strUser)
    return user.sessao
  }

  function getParceiroId(){
    var parceiroID = localStorage.getItem("parceiroID");
    if (!parceiroID){    // se o objeto não existe no localStorage, volta para home.
      window.location = "dashcard.html";
      return;
    }
    //localStorage.removeItem("parceiroID");
    return parceiroID
  }

  function getDetalheParceiro(session, parceiroID)
  {
      var xmlHttp = new XMLHttpRequest();
      var theUrl = 'https://5loarm486l.execute-api.us-east-1.amazonaws.com/dev/agFinanceiros?sessionID='+session+'&id_agente='+parceiroID
      xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
      xmlHttp.send( null );
      if(xmlHttp.status!=200){
        window.location = "index.html";
        return;
      }
      var dadosJson = JSON.parse(xmlHttp.responseText.replaceAll(/'/g,'"'));
      return dadosJson;
  }

  function getUsuario(session)
  {
      var xmlHttp = new XMLHttpRequest();
      var theUrl = 'https://5loarm486l.execute-api.us-east-1.amazonaws.com/dev/usuario?sessionID=' + session
      xmlHttp.open( "GET", theUrl, false ); 
      xmlHttp.send( null );
      if(xmlHttp.status!=200){
        window.location.replace("index.html");
      }
      var dadosJson = JSON.parse(xmlHttp.responseText.replaceAll(/'/g,'"'));
      return dadosJson;
  }
  function atualizaNomeFoto(nome, foto){
    try{
    document.getElementById("nomeUser").textContent = nome; 
    document.getElementById("fotoUser").src = foto; 
    } catch{}
  }

  function logout(){
    localStorage.removeItem("userDASH");
    window.location = "index.html";
    return;
  }

function MontaDadosParceiro(dados){
  document.getElementById("nomeAgt").textContent = dados['nome'];
  document.getElementById("vTrans").textContent = dados['volume'];
  document.getElementById("vSucesso").textContent = dados['sucesso'];
  document.getElementById("vFalhas").textContent = dados['falha'];
  document.getElementById("vFraudes").textContent = dados['fraude'];


}

  var sessionCode = getSession();
  var dadosUser = getUsuario(sessionCode);
  var nomeUser = dadosUser['nome'] + "(" + dadosUser['racf']+ ")";
  var fotoUser = dadosUser['urlFoto'];    
  atualizaNomeFoto(nomeUser,fotoUser);

  var ParceiroId = getParceiroId();
  dados = getDetalheParceiro(sessionCode, ParceiroId);

  MontaDadosParceiro(dados);
