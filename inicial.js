  function getMSG() {
    var url = new URL(window.location.href);
    var msg = "";
    try{
      msg = url.searchParams.get("msg");
    }
    catch{
      msg =""
    }
    finally {
      return msg;
    }
  }

  function exibeInfos(msg) {


    if (msg=="SenhaInvalida"){
        document.getElementById("senhaIncorreta").style.visibility="visible";

    } else{
      document.getElementById("senhaIncorreta").style.visibility="hidden";

    }


    if (msg=="SessaoExpirada"){
       
      document.getElementById("sessaoExpirada").style.visibility="visible";

    }
    else{

      document.getElementById("sessaoExpirada").style.visibility="hidden";

    }

  }


let msg = getMSG();
exibeInfos(msg);




