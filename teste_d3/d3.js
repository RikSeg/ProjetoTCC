//Carrega a tabela
function carregarCSV(nomeArquivo) {
  d3.csv(nomeArquivo)
      .then(function (data) {
          var tabela = d3.select('#tabela_dados');
          
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




// Carregar o Gráfico
    d3.csv("../projecao_multidimensional/output/Saida_t-SNE_GSI002.csv").then(function(data) {
      
     


      // Converter valores de v1 e v2 para números
      data.forEach(function(d) {
        d.v1 = +d.v1;
        d.v2 = +d.v2;
        d.id = d.id;
      });
      
      // Definir margens e dimensões do gráfico
      var margin = {top: 20, right: 20, bottom: 30, left: 40},
          width = 600 - margin.left - margin.right,
          height = 400 - margin.top - margin.bottom;

      // Definir escala x
      var x = d3.scaleLinear()
          .domain(d3.extent(data, function(d) { return d.v1; }))
          .range([0, width-50]);

      // Definir escala y
      var y = d3.scaleLinear()
          .domain(d3.extent(data, function(d) { return d.v2; }))
          .range([height-50, 0]);

      // Definir escala de cores para a classe
      var color = d3.scaleOrdinal(d3.schemeCategory10);

      table = d3.select("#tabela-dados")
      // Criar elemento SVG
      var svg = d3.select("svg")
          .attr("width", width + margin.left + margin.right+100)
          .attr("height", height + margin.top + margin.bottom)
        .append("g")
          .attr("transform",
                "translate(" + margin.left + "," + margin.top + ")");


      // Adicionar círculos
      svg.selectAll("circle")
          .data(data)
        .enter().append("circle")
          .attr("cx", function(d) { return x(d.v1); })
          .attr("cy", function(d) { return y(d.v2); })
          .attr("r", 5) // Raio do círculo
          .style("fill", function(d) { return color(d.class); })
          .attr("id",function(d){return d.id;})
        
          
          // Adicionar brush
          var brush = d3.brush()
              .extent([[-10, -10], [width, height]])
              .on("end", brushed);
          svg.call(brush);
          // Função para lidar com a seleção do brush
          function brushed(event) {
            if (!event.selection) return;
            var [[x0, y0], [x1, y1]] = event.selection;
            
            // Selecionar os pontos dentro da área do brush
            var selectedIds = [];
            svg.selectAll("circle")
                .attr("class", function(d) {
                    var isSelected = x0 <= x(d.v1) && x(d.v1) <= x1 && y0 <= y(d.v2) && y(d.v2) <= y1;
                    if(isSelected) selectedIds.push(d.id);
                    return isSelected ? "selected" : null; 
                });
            var tabela_detalhe = d3.select("#tabela_dados").selectAll("tr").nodes();
          
            // Selecionar as linhas da tabela que correspondem aos pontos selecionados
            var nomesElementos = tabela_detalhe.map(function(elemento) {
              return elemento.getAttribute("id"); // Retorna o nome do nó do elemento (por exemplo, "TR")
          });
          console.log(nomesElementos);

            nomesElementos.forEach(function(d) {
              if(selectedIds.includes(d)){
                d3.select("#tabela_dados").select("tbody").select('[id="'+d+'"]')
                .attr("class","visible");
                
              }else{
                d3.select("#tabela_dados").select("tbody").select('[id="'+d+'"]')
                .attr("class","invisible");
              }
            });
        }
        
      
      // Adicionar eixos visíveis
      //svg.append("g")
      //    .attr("transform", "translate(0," + height + ")")
      //    .call(d3.axisBottom(x));

      //svg.append("g")
      //    .call(d3.axisLeft(y));

    }).catch(function(error) {
      console.log("Erro ao carregar os dados: " + error);
    });