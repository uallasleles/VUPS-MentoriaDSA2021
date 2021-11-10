// CONSTS, VARS
const url = "/api/data";
const tableId = "table";
var jqxhr;

// OBTEM OS DADOS
function getData(sourceName) {
    return $.ajax({
        url: url,
        data: {
            sourceName: sourceName
        },
        type: "GET",
        dataType: "json"
    })
    .done(function(resp){
        trataResposta(resp);
    })
    .fail(function( xhr, status, errorThrown ) {
        alert('Houve um problema com o pedido.');
        console.log( "Error: " + errorThrown );
        console.log( "Status: " + status );
        console.dir( xhr );
    });
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
        searching: true,
        columns: columns,
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

function trataResposta(json) {
    
    // PEGA OS NOMES DAS COLUNAS
    var headerNames = Object.keys(json.data[0]);

    // CHAMA MÉTODO PARA CRIAR CABEÇALHO HTML
    var headerHTML = createHeader(headerNames);

    // ADICIONA O HEADER AO ELEMENTO TABLE
    $(tableId).append(headerHTML);

    var columns = []; // VARIÁVEL PARA DEFINIÇÃO DE COLUNAS DATATABLES
    // PREENCHE A DEFINIÇÃO DE COLUNAS QUE SERÁ ENTREGUE À INSTÂNCIA DATATABLES
    var headerLength = headerNames.length;
    for ( var i = 0; i < headerLength; i++ ){
        columns.push({data: headerNames[i]});    
    };

    // myDataTable.destroy();
    // CRIA UMA INSTÂNCIA DATATABLES
    var myDataTable = $(tableId).DataTable(
        setDataTableDefinitions(columns));

    // ADICIONA OS REGISTROS A INSTÂNCIA DATATABLE E RENDERIZA
    myDataTable.rows.add(json.data).draw();

    // myDataTable.ajax.reload(json.data);
    
};