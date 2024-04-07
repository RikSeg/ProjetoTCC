function carregarCSV(nomeArquivo) {
    d3.csv(nomeArquivo)
        .then(function (data) {
            var tabela = d3.select('#tabela_dados');
            
            console.log(data.columns);
            var colunas = data.columns;


            // Cria o cabeçalho da tabela
            var cabecalho = tabela.select("thead").append('tr');
            data.columns.forEach(function (key) {
                cabecalho.append('th').text(key);
            });

            // Preenche os dados da tabela
            var linhas = tabela.selectAll("tbody")
                .data(data)
                .enter()
                .append('tr')
                .attr('id', function(d) { return d.IDT_MATRICULA; })
                .classed("table",true);

            linhas.selectAll('td')
                .data(function (d) { 
                    return colunas.map(function(column) {
                    return {column: column, value: d[column]};
                }); })
                .enter()
                .append('td')
                .text(function (d) { return d.value; });
        })
        .catch(function (error) {
            console.error('Falha ao carregar o arquivo CSV:', error);
        });
}

// Chame a função passando o nome do arquivo CSV
carregarCSV('../projecao_multidimensional/input/GSI002.csv');