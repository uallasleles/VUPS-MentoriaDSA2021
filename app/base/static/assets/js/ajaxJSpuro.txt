// CONSTS, VARS
const url = "/api/data";
const tableId = "table";
var xhr;

function getData(sourceName){
    
    // 1
    xhr = new XMLHttpRequest(); // criando o objeto de requisição
    
    // 2 - informando ao obj. de solicitação qual função JS tratará a resposta
    xhr.addEventListener("readystatechange", function(resp){
        trataResposta(resp); 
    }, false);

    // 3 
    xhr.responseType = "json";      // definindo o tipo de dado esperado na resposta
    
    // 4
    req = url + "?sourceName=" + sourceName; // se for enviar dados por GET, monta os parâmetros na url
    
    // 5
    xhr.open("GET", req, true);     // abrindo a URL // true para requisição assíncrona
    
    // 6
    xhr.send();                     // enviando a requisição
                    
};

function trataResposta(resp){
    try {
        if(xhr.readyState === XMLHttpRequest.DONE){
            if(xhr.status === 200){

                var json = resp.srcElement.response;
                
                // PEGA OS NOMES DAS COLUNAS
                var headerNames = Object.keys(json.data[0]);
        
                // CHAMA MÉTODO PARA CRIAR CABEÇALHO HTML
                var headerHTML = createHeader(headerNames);
        
                // ADICIONA O HEADER AO ELEMENTO TABLE
                $(tableId).append(headerHTML);
        
                var columns = []; // VARIÁVEL PARA DEFINIÇÃO DE COLUNAS DATATABLES
                // PREENCHE A DEFINIÇÃO DE COLUNAS QUE SERÁ ENTREGUE À INSTÂNCIA DATATABLES
                var headersLength = headerNames.length;
                for ( var i = 0; i < headersLength; i++ ){
                    columns.push({data: headerNames[i]});    
                };
        
                // myDataTable.destroy();
                // CRIA UMA INSTÂNCIA DATATABLES
                var myDataTable = $(tableId).DataTable(
                    setDataTableDefinitions(columns));
        
                // ADICIONA OS REGISTROS A INSTÂNCIA DATATABLE E RENDERIZA
                myDataTable.rows.add(json.data).draw();
        
                // myDataTable.ajax.reload(json.data);
                
            } else {
                alert('Houve um problema com o pedido.');
            }
        }                
    }
    catch(e){
        alert('Exceção Capturada: ' + e.description);
    }
};

// CRIA E RETORNA UM CABEÇALHO HTML DE ACORDO COM A LISTA DE NOMES DE COLUNAS INFORMADA
function createHeader(columnNames) {
    var myTable = document.getElementById(tableId);     // CRIA UMA INSTÂNCIA DO ELEMENTO TABLE        
    var tableHead = document.createElement("thead");    // CRIA UM NÓ TABLE HEAD
    var tableRow = document.createElement("tr");        // CRIA UM NÓ TABLE ROW
    
    while (tableRow.firstChild){    // Removendo todos os nós filhos da linha
        tableRow.removeChild(tableRow.firstChild);};
    while (tableHead.firstChild){   // Removendo todos os nós filhos do cabeçalho
        tableHead.removeChild(tableHead.firstChild);};
    while (myTable.firstChild) {    // Removendo todos os nós filhos da tabela
        var h = myTable.removeChild(myTable.firstChild);};

    // ADICIONA TABLE HEADING COM O NOME DA COLUNA PARA A TABLE ROW
    var columnsLength = columnNames.length;
    for (var i = 0; i < columnsLength; i++) {
        var headerCell = document.createElement("th");
        headerCell.innerHTML = columnNames[i];
        tableRow.appendChild(headerCell);
    };
    tableHead.appendChild(tableRow);
    
    return tableHead;
};

// CONFIGURA OPÇÕES PARA INICIALIZAÇÃO DA INSTÂNCIA DATATABLE
function setDataTableDefinitions(columns) {

    var dataTableSetup = {
        // dom: "Bfrtip",
        // ajax: urlstr,
        processing: true,
        // serverSide: true,
        // dataSrc: 'data',
        responsive: true,
        // sort: true,
        // lengthMenu: [[5, 10, 25, 50, -1], [5, 10, 25, 50, "All"]],
        searching: true,
        // columnDefs: columnDefs,
        columns: columns,
        // paging: false,
        // info: false,
        scrollX: true,
        scrollY: 350,
        language: {
            processing: "Processando a solicitação ...",
            zeroRecords: "Não há registros para exibir",
        }
        // destroy: true
    };
    return dataTableSetup;
};