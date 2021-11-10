// // cria um objeto que possui uma seleção de elementos com essa classe dropdown-item
// var oDropdownItem = document.getElementsByClassName("dropdown-item");
// // percorre os índices das opções
// for(i in oDropdownItem){
//     // trata o texto de cada opção, remove quebras de linha e espaços
//     let item = oDropdownItem[i].text.replace(/^\s+|\s+$/gm,'').trim();
//     // adiciona uma espera de evento onclick para cada opção do dropdown
//     oDropdownItem[i].addEventListener("click", function(){ // função de callback
        
//         // processamento quando o click ocorrer
//         tgt = "/tbl_"+item+".html"; // monta uma url
//         window.location.href = tgt; // faz o redirecionamento
    
//     });
// };

// OBTEM OPÇÃO SELECIONADA EM DROPDOWN ITEM
$(".dropdown-item").on('click', function() {
    // OBTEM OPÇÃO SELECIONADA EM DROPDOWN ITEM
    var item = $(this).text().trim();
    tgt = "/tbl_"+item+".html"; // monta uma url
    window.location.href = tgt;
});