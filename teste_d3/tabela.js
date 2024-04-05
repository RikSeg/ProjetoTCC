function carregarCSV(nomeArquivo) {
    d3.csv(nomeArquivo)
        .then(function (data) {
            var tabela = d3.select('#tabela_dados');
            
            // Limpa o conteúdo atual da tabela
            tabela.selectAll('*').remove();

            // Cria o cabeçalho da tabela
            var cabecalho = tabela.append('tr');
            Object.keys(data[0]).forEach(function (key) {
                cabecalho.append('th').text(key);
            });

            // Preenche os dados da tabela
            var linhas = tabela.selectAll('tr')
                .data(data)
                .enter()
                .append('tr');

            linhas.selectAll('td')
                .data(function (d) { return Object.values(d); })
                .enter()
                .append('td')
                .text(function (d) { return d; });
        })
        .catch(function (error) {
            console.error('Falha ao carregar o arquivo CSV:', error);
        });
}

// Chame a função passando o nome do arquivo CSV
carregarCSV('../projecao_multidimensional/input/GSI002.csv');