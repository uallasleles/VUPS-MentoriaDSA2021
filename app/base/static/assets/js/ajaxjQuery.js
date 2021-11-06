// CONSTS, VARS
var urlstr = "/api/data";
var count = 0;
const tableId = "table";

// OBTEM OS DADOS
function getData(sourceName) {
    return $.ajax({
        url: urlstr,
        data: {
            sourceName: sourceName
        }
    });
};

// CRIA E RETORNA UM CABEÇALHO HTML DE ACORDO COM A LISTA DE NOMES DE COLUNAS INFORMADA
function createHeader(columnNames) {
    var myTable = document.getElementById(tableId);     // CRIA UMA INSTÂNCIA DO ELEMENTO TABLE        
    var tableHead = document.createElement("thead");    // CRIA UM NÓ TABLE HEAD
    var tableRow = document.createElement("tr");        // CRIA UM NÓ TABLE ROW

    // ADICIONA TABLE HEADING COM O NOME DA COLUNA PARA A TABLE ROW
    for (var i = 0; i < columnNames.length; i++) {
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
        dataSrc: 'data',
        responsive: true,
        sort: true,
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

// OBTEM OPÇÃO SELECIONADA EM DROPDOWN ITEM
$(".dropdown-item").on('click', function() {
    // OBTEM OPÇÃO SELECIONADA EM DROPDOWN ITEM
    var sourceName = $(this).text().trim();
    tgt = "/"+sourceName+".html";
    window.location.href = tgt;
});

function dataset(){

    var sourceName = 'transferencias';
    
    // CHAMA A O MÉTODO PARA OBTER OS DADOS
    getData(sourceName).done( function(json) {

        // PEGA OS NOMES DAS COLUNAS
        var headerNames = Object.keys(json.data[0]);

        // CHAMA MÉTODO PARA CRIAR CABEÇALHO HTML
        var headerHTML = createHeader(headerNames);

        // ADICIONA O HEADER AO ELEMENTO TABLE
        $(tableId).append(headerHTML);

        var columns = []; // VARIÁVEL PARA DEFINIÇÃO DE COLUNAS DATATABLES
        // PREENCHE A DEFINIÇÃO DE COLUNAS QUE SERÁ ENTREGUE À INSTÂNCIA DATATABLES
        for ( var i = 0; i < headerNames.length; i++ ){
            columns.push({data: headerNames[i]});    
        };

        // CRIA UMA INSTÂNCIA DATATABLES
        var myDataTable = $(tableId).DataTable(
            setDataTableDefinitions(columns));

        // ADICIONA OS REGISTROS A INSTÂNCIA DATATABLE E RENDERIZA
        myDataTable.rows.add(json.data).draw();
            
    });
};