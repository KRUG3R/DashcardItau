
  function httpGet(session)
  {
      var xmlHttp = new XMLHttpRequest();
      var theUrl = 'http://localhost:8000/parceiros?sessionCode=' + session
      xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
      xmlHttp.send( null );
      alert(xmlHttp.responseText);
      return xmlHttp.responseText;
  }

  function getSession() {
    var url = new URL(window.location.href);
    var session = url.searchParams.get("sessionCode");
    return session
}
