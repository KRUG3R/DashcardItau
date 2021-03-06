
  function httpGet(session)
  {
      var xmlHttp = new XMLHttpRequest();
      let url = 'httpGet("localhost:8000/parceiros?sessionCode=' + session
      xmlHttp.open( "GET",url , false );
      xmlHttp.send( null );
      alert(xmlHttp.responseText);
      return xmlHttp.responseText;
  }

  function getSession() {
    var url = new URL(window.location.href);
    var session = url.searchParams.get("sessionCode");
    return session
}
