// Adiciona o evento de clique ao botão usando D3.js
d3.select('#limparClasses').on('click', function() {
    // Seleciona todos os elementos com a classe 'elemento' usando D3.js
    d3.select('tbody').selectAll('tr')
        .attr('class', ''); // Remove todas as classes exceto a classe 'elemento'
});