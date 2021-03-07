
  function httpGetAgentesFin(session)
  {
      var xmlHttp = new XMLHttpRequest();
      var theUrl = 'http://localhost:8000/parceiros?sessionCode=' + session
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

function atualizaNomeFoto(nome,foto,sessao) {
  document.getElementById("nome").textContent = nome; 
  document.getElementById("foto").src = foto; 
  document.getElementById("sessionCode").value=sessao;
}

function geraComboBox(data) {
  let select = document.getElementById("CBparceiro");
  for (let element of data) {
    var option = document.createElement('option');
    option.value = element[0];
    option.text = element[1];
    select.add(option);
  }
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
      let text = document.createTextNode(element[key]);
      cell.appendChild(text);
    }
  }
}

let sessao = getSession();
let dados = httpGetAgentesFin(sessao);

let nome = dados['usuario']['nome'] + "(" + dados['usuario']['racf']+ ")";
let foto = dados['usuario']['urlFoto'];
atualizaNomeFoto(nome,foto,sessao);

dadosCB = dados['Agentes'];
geraComboBox(dadosCB);

dadosTB = dados['Top10'];
generateTableHead(dadosTB);
generateTable(dadosTB);




