// Carregar o arquivo CSV
    d3.csv("../projecao_multidimensional/output/Saida_t-SNE_GSI002.csv").then(function(data) {
      
      // Converter valores de v1 e v2 para números
      data.forEach(function(d) {
        d.v1 = +d.v1;
        d.v2 = +d.v2;
      });
      
      // Definir margens e dimensões do gráfico
      var margin = {top: 20, right: 20, bottom: 30, left: 40},
          width = 800 - margin.left - margin.right,
          height = 600 - margin.top - margin.bottom;

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

      // Criar elemento SVG
      var svg = d3.select("svg")
          .attr("width", width + margin.left + margin.right+200)
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
          .on("mouseover", function(event, d) {
            // Mostrar rótulo ao passar o mouse sobre o círculo
            var tooltip = svg.append("g")
              .attr("class", "tooltip");
              

            var text = tooltip.append("text")
              .attr("x", x(d.v1) + 10)
              .attr("y", y(d.v2) - 10)
              .text(d.id+" "+d.class);

            var bbox = text.node().getBBox(); // Obtém a caixa delimitadora do texto
            var padding = 5; // Espaçamento entre o texto e a borda do retângulo

            tooltip.insert("rect", "text") // Insere o retângulo antes do texto
              .attr("x", bbox.x - padding)
              .attr("y", bbox.y - padding)
              .attr("width", bbox.width + 2 * padding)
              .attr("height", bbox.height + 2 * padding)
              .style("fill", "lightgray")
              .style("stroke", "black");
          })
          .on("mouseout", function() {
            // Remover rótulo ao retirar o mouse do círculo
            d3.selectAll(".tooltip").remove();
          });
          

          // Adicionar brush
         // var brush = d3.brush()
         //     .extent([[0, 0], [width, height]])
         //     .on("end", brushed);
         // svg.call(brush);
         // // Função para lidar com a seleção do brush
         // function brushed(event) {
         //   if (!event.selection) return;
         //   var [[x0, y0], [x1, y1]] = event.selection;
         //   svg.selectAll("circle")
         //     .classed("selected", d => x0 <= x(d.v1) && x(d.v1) <= x1 && y0 <= y(d.v2) && y(d.v2) <= y1)
         //     
         // }


      
      // Adicionar eixos visíveis
      //svg.append("g")
      //    .attr("transform", "translate(0," + height + ")")
      //    .call(d3.axisBottom(x));

      //svg.append("g")
      //    .call(d3.axisLeft(y));

    }).catch(function(error) {
      console.log("Erro ao carregar os dados: " + error);
    });