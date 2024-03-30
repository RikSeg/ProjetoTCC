// Função para carregar o arquivo CSV e criar a tabela
function carregarCSV(nomeArquivo) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                var linhas = xhr.responseText.trim().split('\n');
                var tabela = document.getElementById('tabela_dados');
                tabela.innerHTML = ''; // Limpa o conteúdo atual da tabela
                var cabecalho = linhas[0].split(',');
                var htmlCabecalho = '<tr>';
                for (var i = 0; i < cabecalho.length; i++) {
                    htmlCabecalho += '<th>' + cabecalho[i] + '</th>';
                }
                htmlCabecalho += '</tr>';
                tabela.innerHTML += htmlCabecalho;
                for (var j = 1; j < linhas.length; j++) {
                    var colunas = linhas[j].split(',');
                    var htmlLinha = '<tr>';
                    for (var k = 0; k < colunas.length; k++) {
                        htmlLinha += '<td>' + colunas[k] + '</td>';
                    }
                    htmlLinha += '</tr>';
                    tabela.innerHTML += htmlLinha;
                }
            } else {
                console.error('Falha ao carregar o arquivo CSV.');
            }
        }
    };
    xhr.open('GET', nomeArquivo, true);
    xhr.send();
}

// Chame a função passando o nome do arquivo CSV
carregarCSV('../projecao_multidimensional/input/iris_index.csv');