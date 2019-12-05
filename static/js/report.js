var json_data;

$(document).ready(function() {
    $('.list').hide();
    $('#get_chart').click(function() {
        var selected = $('#graph').val();
        var selected_chart = '';
        if (selected == 'State') {
            selected_chart = $('#inputState').val();
            url = '/ajax-state-report/' + selected_chart;
        } else if (selected == 'City') {
            selected_chart = $('#inputCity').val();
            url = '/ajax-city-report/' + selected_chart;
        } else {
            selected_chart = selected;
            url = '/ajax-user-report/' + selected_chart;
        }
        $.ajax({
            url: url,
            type: 'GET',
            dataType: 'JSON',
            success: function(response) {
            console.log(response)
                generate_graph(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});

$(document).change(function() {
    $('.state').hide();
    $('.city').hide();
    var selected = $('#graph').val();
    if (selected == 'State') {
        $('.state').show();
    } else if (selected == 'City') {
        $('.city').show();
    }
});



//Read the data
function generate_graph(data) {

  //Clear the svg before loading
  d3.selectAll('svg > g > *').remove();

  height = 700;
  width = 1000;

  margin = ({top: 20, right: 20, bottom: 30, left: 30})

  x = d3.scaleUtc()
    .domain(d3.extent(data.dates))
    .range([margin.left, width - margin.right])

  y = d3.scaleLinear()
    .domain([0, d3.max(data.series, d => d3.max(d.values))]).nice()
    .range([height - margin.bottom, margin.top])

  xAxis = g => g
    .attr("transform", `translate(0,${height - margin.bottom})`)
    .call(d3.axisBottom(x).ticks(width / 80).tickSizeOuter(0))

  yAxis = g => g
    .attr("transform", `translate(${margin.left},0)`)
    .call(d3.axisLeft(y))
    .call(g => g.select(".domain").remove())
    .call(g => g.select(".tick:last-of-type text").clone()
        .attr("x", 3)
        .attr("text-anchor", "start")
        .attr("font-weight", "bold")
        .text(data.y))

  line = d3.line()
    .defined(d => !isNaN(d))
    .x((d, i) => x(data.dates[i]))
    .y(d => y(d))

  const svg = d3.select("svg")
     .attr("viewBox", [0, 0, width, height]);

  svg.append("g")
      .call(xAxis);

  svg.append("g")
      .call(yAxis);

//Create Title
  svg.append("text")
	 .attr("x", width / 2 )
     .attr("y", 50)
     .style("text-anchor", "middle")
     .text("Daily Water Usage Report in Gallons");

  const path = svg.append("g")
      .attr("fill", "none")
      .attr("stroke", "steelblue")
      .attr("stroke-width", 1.5)
      .attr("stroke-linejoin", "round")
      .attr("stroke-linecap", "round")
    .selectAll("path")
    .data(data.series)
    .join("path")
      .style("mix-blend-mode", "multiply")
      .attr("d", d => line(d.values));


  svg.call(hover, path);


  function hover(svg, path) {
      svg.style("position", "relative");

      if ("ontouchstart" in document) svg
          .style("-webkit-tap-highlight-color", "transparent")
          .on("touchmove", moved)
          .on("touchstart", entered)
          .on("touchend", left)
      else svg
          .on("mousemove", moved)
          .on("mouseenter", entered)
          .on("mouseleave", left);

      const dot = svg.append("g")
          .attr("display", "none");

      dot.append("circle")
          .attr("r", 2.5);

      dot.append("text")
          .style("font", "10px sans-serif")
          .attr("text-anchor", "middle")
          .attr("y", -8);

      function moved() {
        d3.event.preventDefault();
        const ym = y.invert(d3.event.layerY);
        const xm = x.invert(d3.event.layerX);
        const i1 = d3.bisectLeft(data.dates, xm, 1);
        const i0 = i1 - 1;
        const i = xm - data.dates[i0] > data.dates[i1] - xm ? i1 : i0;
        const s = data.series.reduce((a, b) => Math.abs(a.values[i] - ym) < Math.abs(b.values[i] - ym) ? a : b);
        path.attr("stroke", d => d === s ? null : "#ddd").filter(d => d === s).raise();
        dot.attr("transform", `translate(${x(data.dates[i])},${y(s.values[i])})`);
        dot.select("text").text(s.name);
      }

      function entered() {
        path.style("mix-blend-mode", null).attr("stroke", "#ddd");
        dot.attr("display", null);
      }

      function left() {
        path.style("mix-blend-mode", "multiply").attr("stroke", null);
        dot.attr("display", "none");
      }
  }

  return svg.node();
}
