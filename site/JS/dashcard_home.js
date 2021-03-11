function getSession(){
  var strUser = localStorage.getItem("userDASH");
  if (!strUser){    // se o objeto não existe no localStorage, signifca que eu não estou conectado
    window.location = "index.html";
    return;
  }
  var user = JSON.parse(strUser)
  return user.sessao
}

function detalhe(){
  //alert(document.getElementById("CBparceiro").value);
  var valor=document.getElementById("CBparceiro").value
  localStorage.setItem("parceiroID", valor)
  window.location = "detalheAgente.html";
  return;

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

function getTop10(session)
{
    
    var xmlHttp = new XMLHttpRequest();
    var theUrl = 'https://5loarm486l.execute-api.us-east-1.amazonaws.com/dev/agFinanceiros/top10?sessionID=' + session
    xmlHttp.open( "GET", theUrl, false ); 
    xmlHttp.send( null );
    if(xmlHttp.status!=200){
      window.location.replace("index.html");
    }
   
    var dadosJson = JSON.parse(xmlHttp.responseText.replaceAll(/'/g,'"'));
    return dadosJson;
}


function getAgentes(session)
{
    var xmlHttp = new XMLHttpRequest();
    var theUrl = 'https://5loarm486l.execute-api.us-east-1.amazonaws.com/dev/agFinanceiros?sessionID=' + session
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

function geraComboBox(data) {
  try{
    let select = document.getElementById("CBparceiro");
    for (let element of data) {
      var option = document.createElement('option');
      option.value = element['id_agente'];
      option.text = element['nome_agente'];
      select.add(option);
    }
  } catch{}
}



function generateTableHead(data) {
  let keys = Object.keys(data[0]);
  let table = document.getElementById("tabelaParceiros");
  let thead = table.createTHead();
  let row = thead.insertRow();
  
  for (let key of keys) {
    let th = document.createElement("th");
    let text = document.createTextNode(key);
    th.appendChild(text);
    row.appendChild(th);
  }
}

function generateTable(data) {
  table = document.getElementById("tabelaParceiros");
  for (let element of data) {
    let row = table.insertRow();
    for (key in element) {
      let cell = row.insertCell();
      let text = document.createTextNode(element[key] );
      cell.appendChild(text);
      
    }
  }
}

function logout(){
  localStorage.removeItem("userDASH");
  window.location = "index.html";
  return;
}

var sessionCode = getSession();
var dadosUser = getUsuario(sessionCode);
var nomeUser = dadosUser['nome'] + "(" + dadosUser['racf']+ ")";
var fotoUser = dadosUser['urlFoto'];
var dadosCB = getAgentes(sessionCode);
var dadosTB = getTop10(sessionCode);

generateTableHead(dadosTB);
generateTable(dadosTB);
geraComboBox(dadosCB);
atualizaNomeFoto(nomeUser,fotoUser);





