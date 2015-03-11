var color_range = ["#0ed369", "#ff9a90", "#dddddd"];



var draw_rot_vis = function() {

    var margin = {top: 20, right: 20, bottom: 30, left: 40},
        width = 960 - margin.left - margin.right,
        height = 500 - margin.top - margin.bottom;

    var x = d3.scale.ordinal()
        .rangeRoundBands([0, width], .1);

    var y = d3.scale.linear()
        .rangeRound([height, 0]);

    var color = d3.scale.ordinal()
        .range(color_range);

    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom");

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left")
        .tickFormat(d3.format(".1s"));

    var svg = d3.select(".rot-vis-container").append("svg")
        .attr("width", "100%")
        .attr('viewBox', '0 0 ' + String(width + margin.left + margin.right) + ' ' + String(height + margin.top + margin.bottom))
        .attr('perserveAspectRatio', 'none')
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    d3.csv("d3-data/year-rot-d3.csv", function(error, data) {
      color.domain(d3.keys(data[0]).filter(function(key) { return key !== "Year"; }));

      data.forEach(function(d) {
        var y0 = 0;
        d.ages = color.domain().map(function(name) { return {name: name, y0: y0, y1: y0 += +d[name]}; });
        d.total = d.ages[d.ages.length - 1].y1;
      });

      //data.sort(function(a, b) { return b.total - a.total; });

      x.domain(data.map(function(d) { return d.Year; }));
      y.domain([0, d3.max(data, function(d) { return d.total; })]);

      svg.append("g")
          .attr("class", "x axis")
          .attr("transform", "translate(0," + height + ")")
          .attr("fill", "#555")
          .call(xAxis);

      svg.append("g")
          .attr("class", "y axis")
          .call(yAxis)
        .append("text")
          .attr("transform", "rotate(-90)")
          .attr("y", 6)
          .attr("dy", ".71em")
          .style("text-anchor", "end")
          .attr("fill", "#555")
          .text("Citation to the Web");

      var state = svg.selectAll(".state")
          .data(data)
        .enter().append("g")
          .attr("class", "g")
          .attr("transform", function(d) { return "translate(" + x(d.Year) + ",0)"; });

      state.selectAll("rect")
          .data(function(d) { return d.ages; })
        .enter().append("rect")
          .attr("width", x.rangeBand())
          .attr("y", function(d) { return y(d.y1); })
          .attr("height", function(d) { return y(d.y0) - y(d.y1); })
          .style("fill", function(d) { return color(d.name); });

      var legend = svg.selectAll(".legend")
          .data(color.domain().slice().reverse())
        .enter().append("g")
          .attr("class", "legend")
          .attr("transform", function(d, i) { return "translate(-550," + i * 20 + ")"; });

      legend.append("rect")
          .attr("x", width - 18)
          .attr("width", 18)
          .attr("height", 18)
          .style("fill", color);

      legend.append("text")
          .attr("x", width - 24)
          .attr("y", 9)
          .attr("dy", ".35em")
          .style("text-anchor", "end")
          .text(function(d) { return d; });

    });


}

var draw_rot_100_vis = function() {

    var margin = {top: 20, right: 185, bottom: 30, left: 40},
        width = 960 - margin.left - margin.right,
        height = 500 - margin.top - margin.bottom;

    var x = d3.scale.ordinal()
        .rangeRoundBands([0, width], .1);

    var y = d3.scale.linear()
        .rangeRound([height, 0]);

    var color = d3.scale.ordinal()
        .range(color_range);

    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom");

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left")
        .tickFormat(d3.format(".0%"));

    var svg = d3.select(".rot-vis-100-container").append("svg")
        .attr("width", "100%")
        .attr('viewBox', '0 0 ' + String(width + margin.left + margin.right) + ' ' + String(height + margin.top + margin.bottom))
        .attr('perserveAspectRatio', 'none')
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    d3.csv("d3-data/year-rot-d3.csv", function(error, data) {
      color.domain(d3.keys(data[0]).filter(function(key) { return key !== "Year"; }));

      data.forEach(function(d) {
        var y0 = 0;
        d.ages = color.domain().map(function(name) { return {name: name, y0: y0, y1: y0 += +d[name]}; });
        d.ages.forEach(function(d) { d.y0 /= y0; d.y1 /= y0; });
      });

      //data.sort(function(a, b) { return b.ages[0].y1 - a.ages[0].y1; });

      x.domain(data.map(function(d) { return d.Year; }));

      svg.append("g")
          .attr("class", "x axis")
          .attr("transform", "translate(0," + height + ")")
          .call(xAxis);

      svg.append("g")
          .attr("class", "y axis")
          .call(yAxis);

      var state = svg.selectAll(".state")
          .data(data)
        .enter().append("g")
          .attr("class", "state")
          .attr("transform", function(d) { return "translate(" + x(d.Year) + ",0)"; });

      state.selectAll("rect")
          .data(function(d) { return d.ages; })
        .enter().append("rect")
          .attr("width", x.rangeBand())
          .attr("y", function(d) { return y(d.y1); })
          .attr("height", function(d) { return y(d.y0) - y(d.y1); })
          .style("fill", function(d) { return color(d.name); });

      var legend = svg.select(".state:last-child").selectAll(".legend")
          .data(function(d) { return d.ages; })
        .enter().append("g")
          .attr("class", "legend")
          .attr("transform", function(d) { return "translate(" + x.rangeBand() / 2 + "," + y((d.y0 + d.y1) / 2) + ")"; });

      legend.append("line")
          .attr("x2", 10);

      legend.append("text")
          .attr("x", 13)
          .attr("dy", ".35em")
          .text(function(d) { return d.name; });
    });
}




var draw_archive_dist_per_year = function() {

var radius = 84,
    padding = 10;

var color = d3.scale.ordinal()
    .range(["#0074D9", "#3D9970", "#2ECC40", "#FFDC00", "#FF851B", "#B10DC9", "#F012BE", "#FF4136"]);

var arc = d3.svg.arc()
    .outerRadius(radius)
    .innerRadius(radius - 30);

var pie = d3.layout.pie()
    .sort(null)
    .value(function(d) { return d.population; });

d3.csv("d3-data/archive-dist-d3.csv", function(error, data) {
    color.domain(d3.keys(data[0]).filter(function(key) { return key !== "Year"; }));

    data.forEach(function(d) {
      d.ages = color.domain().map(function(name) {
        return {name: name, population: +d[name]};
      });
    });

    

    var svg = d3.select(".archive-dist-container").selectAll(".pie")
        .data(data)
      .enter().append("svg")
        .attr("class", "pie")
        .attr("width", radius * 2)
        .attr("height", radius * 2)
      .append("g")
        .attr("transform", "translate(" + radius + "," + radius + ")");

    svg.selectAll(".arc")
        .data(function(d) { return pie(d.ages); })
      .enter().append("path")
        .attr("class", "arc")
        .attr("d", arc)
        .style("fill", function(d) { return color(d.data.name); });

    svg.append("text")
        .attr("dy", ".35em")
        .style("text-anchor", "middle")
        .text(function(d) { return d.Year; });


    var legend = d3.select(".archive-dist-container").append("svg")
        .attr("class", "legend")
        .attr("width", radius * 2)
        .attr("height", radius * 2)
      .selectAll("g")
        .data(color.domain().slice().reverse())
      .enter().append("g")
        .attr("transform", function(d, i) { return "translate(20," + i * 12 + ")"; });

    legend.append("rect")
        .attr("width", 20)
        .attr("height", 10)
        .style("fill", color);

    legend.append("text")
        .attr("x", 24)
        .attr("y", 5)
        .attr("dy", ".35em")
        .text(function(d) { return d; });

});

}









$( document ).ready(function() {





























draw_rot_vis();

draw_rot_100_vis();


draw_archive_dist_per_year();

});













