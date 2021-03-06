

  function generateTableHead(table, data) {
    let thead = table.createTHead();
    let row = thead.insertRow();
    for (let key of data) {
      let th = document.createElement("th");
      let text = document.createTextNode(key);
      th.appendChild(text);
      row.appendChild(th);
    }
  }

  function generateTable(table, data) {
    for (let element of data) {
      let row = table.insertRow();
      for (key in element) {
        let cell = row.insertCell();
        let text = document.createTextNode(element[key]);
        cell.appendChild(text);
      }
    }
  }
  

  function generateSelect(select, data) {
    for (let element of data) {
      var option = document.createElement('option');
      option.text = option.value = element;
      select.add(option, 0);
    }
  }

  let table = document.getElementById("tabelaParceiros");
  let data = Object.keys(top10parceiro[0]);
  generateTableHead(table, data);
  generateTable(table, top10parceiro);
  
  let select = document.getElementById("CBparceiro");
  generateSelect(select, ListParceiro);