// Largura e altura do gráfico
var width = 600;
var height = 400;

// Margens do gráfico
var margin = { top: 50, right: 50, bottom: 50, left: 50 };

// Largura e altura do gráfico sem margens
var innerWidth = width - margin.left - margin.right;
var innerHeight = height - margin.top - margin.bottom;

// Selecionar o elemento onde queremos adicionar o gráfico de dispersão
var svg = d3.select("#scatterplot")
    .append("svg")
    .attr("width", width)
    .attr("height", height);

// Criar um grupo para os pontos de dados
var g = svg.append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// Carregar os dados do arquivo CSV
d3.csv("Saida_ISOMAP.csv").then(function(data) {

    // Converter os dados de string para número
    data.forEach(function(d) {
        d.x = +d.x;
        d.y = +d.y;
    });

    // Criar escalas para os eixos x e y
    var xScale = d3.scaleLinear()
        .domain(d3.extent(data, function(d) { return d.x; }))
        .range([0, innerWidth]);

    var yScale = d3.scaleLinear()
        .domain(d3.extent(data, function(d) { return d.y; }))
        .range([innerHeight, 0]);

    // Adicionar os pontos de dados ao gráfico
    g.selectAll("circle")
        .data(data)
        .enter().append("circle")
        .attr("cx", function(d) { return xScale(d.x); })
        .attr("cy", function(d) { return yScale(d.y); })
        .attr("r", 5) // raio dos pontos
        .style("fill", "steelblue");

    // Adicionar eixos x e y ao gráfico
    g.append("g")
        .attr("transform", "translate(0," + innerHeight + ")")
        .call(d3.axisBottom(xScale));

    g.append("g")
        .call(d3.axisLeft(yScale));

    // Adicionar rótulos aos eixos
    g.append("text")
        .attr("text-anchor", "middle")
        .attr("transform", "translate(" + -40 + "," + (innerHeight / 2) + ")rotate(-90)")
        .text("Eixo Y");

    g.append("text")
        .attr("text-anchor", "middle")
        .attr("transform", "translate(" + (innerWidth / 2) + "," + (innerHeight + 40) + ")")
        .text("Eixo X");

}).catch(function(error) {
    console.log(error);
});
