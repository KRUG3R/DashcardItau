function enviar(){
   
  var usuario = document.getElementById("txtLogin").value;
  var senha = document.getElementById("senha").value;

  
  var myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");
  
  var raw = JSON.stringify({"usuario":usuario,"senha":senha});
  
  var requestOptions = {
    method: 'POST',
    headers: myHeaders,
    body: raw,
    redirect: 'follow'
  };
  
  fetch("https://5loarm486l.execute-api.us-east-1.amazonaws.com/dev/usuario/logon", requestOptions)
    .then(response => trataResultado(response))
    .then(result => console.log(result))
    .catch(error => console.log('error', error));

}

function trataResultado(resultado){
  if (resultado.status==200){
      resultado.json().then(usuario =>
          {
              localStorage.setItem("userDASH", JSON.stringify(usuario));
              window.location="dashcard.html"
          }
          
          
          );
      console.log("acesso ok"+ resultado.body)
  }
  else if(resultado.status==401){
    document.getElementById("senhaIncorreta").style.visibility="visible";
  }

}

function fechar(){
  document.getElementById("senhaIncorreta").style.visibility="hidden";
}

