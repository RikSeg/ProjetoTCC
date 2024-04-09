function carregarCSV(nomeArquivo) {
    d3.csv(nomeArquivo)
        .then(function (data) {
            var tabela = d3.select('#tabela_dados');
            
            console.log(data.columns);
            var colunas = data.columns;


            // Cria o cabeçalho da tabela
            var cabecalho = tabela.select("#titulo_tabela").append('tr').attr("id","head");
            data.columns.forEach(function (key) {
                cabecalho.append('th').text(key);
            });

            tbody = tabela.select("#corpo_tabela");
            
            if (tbody.empty()) {
                tbody = tabela.append("#corpo_tabela");
            }
            // Preenche os dados da tabela
            var linhas = tbody.selectAll("tr")
                .data(data)
                .enter()
                .append('tr')
                .attr('id', function(d) { return d.IDT_MATRICULA; })

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