var json_data;

$(document).ready(function() {
    $('.list').hide();
    $('#get_chart').click(function() {
        var selected = $('#graph').val();
        var selected_chart = '';
        if (selected == 'State') {
            selected_chart = $('#inputState').val();
            url = '/ajax-state-report/' + selected_chart;
        } else {
            selected_chart = $('#inputCity').val();
            url = '/ajax-city-report/' + selected_chart;
        }
        $.ajax({
            url: url,
            type: 'GET',
            dataType: 'JSON',
            success: function(response) {
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
    } else {
        $('.city').show();
    }
});



//Read the data
function generate_graph(data) {

    //Clear the svg before loading
    d3.selectAll('svg > g > *').remove();
    // Draw a line chart
    var svg = d3.select('svg'),
      margin = { top: 20, right: 50, bottom: 30, left: 50 },
      width = +svg.attr('width') - margin.left - margin.right,
      height = +svg.attr('height') - margin.top - margin.bottom,
      g = svg.append('g').attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');
    // Graph title
    g.append('text')
      .attr('x', (width / 2))
      .attr('y', 0 - (margin.top / 3))
      .attr('text-anchor', 'middle')
      .style('font-size', '16px')
      .text('Water usage chart');
    // Function to convert a string into a time
    var parseTime = d3.time.format('%Y-%m-%d').parse;
    // Function to show specific time format
    var formatTime = d3.time.format('%e %B');

    // Set the X scale
    var x = d3.time.scale().range([0, width], 0.5);
    // Set the Y scale
    var y = d3.scale.linear().range([height, 0]);
    // Set the color scale
    var color = d3.scale.category10();

    var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

    var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left");


    function sortByDates(a, b) {
        return new Date(a.Time) - new Date(b.Time);
    }
    data = data.sort(sortByDates);

      // load the data
    {
      // Select the important columns
      color.domain(d3.keys(data[7]).filter(function(key) {
          return key !== "Time" && key !== "_id";
      }));
      // Correct the types
      data.forEach(function(d) {
        console.log(d.Time);
        d.date = parseTime(d.Time);
        console.log("second "+d.date);
      });
      console.log(data);

      var water_usages = color.domain().map(function(name) {
        return {
          name: name,
          values: data.map(function(d) {
            return {
              date: d.date,
              worth: +d[name]
            };
          })
        };
      });
      console.log(water_usages)
      // Set the X domain
      x.domain(d3.extent(data, function(d) {
        return d.date;
      }));

    var line = d3.svg.line()
    // .interpolate("basis")
    .x(function(d) {
      return x(d.date);
    })
    .y(function(d) {
      return y(d.worth);
    });

      // Set the Y domain
      y.domain([
        d3.min(water_usages, function(c) {
          return d3.min(c.values, function(v) {
            return v.worth;
          });
        }),
        d3.max(water_usages, function(c) {
          return d3.max(c.values, function(v) {
            return v.worth;
          });
        })
      ]);
      // Set the X axis
      g.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);
      // Set the Y axis
      g.append("g")
        .attr("class", "y axis")
        .call(yAxis)
        .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("Water Usage (Gal)");

      // Draw the lines
      var water_usage = g.selectAll(".water_usage")
        .data(water_usages)
        .enter().append("g")
        .attr("class", "water_usage");

      water_usage.append("path")
        .attr("class", "line")
        .attr("d", function(d) {
          return line(d.values);
        })
        .style("stroke", function(d) {
          return color(d.name);
        });
      // Add the circles
      water_usage.append("g").selectAll("circle")
        .data(function(d){return d.values})
        .enter()
        .append("circle")
        .attr("r", 2)
        .attr("cx", function(dd){return x(dd.date)})
        .attr("cy", function(dd){return y(dd.worth)})
        .attr("fill", "none")
        .attr("stroke", function(d){return color(this.parentNode.__data__.name)});
      // Add label to the end of the line
      water_usage.append("text")
        .attr("class", "label")
        .datum(function (d) {
          return {
            name: d.name,
            value: d.values[d.values.length - 1]
          };
        })
        .attr("transform", function (d) {
          return "translate(" + x(d.value.date) + "," + y(d.value.worth) + ")";
        })
        .attr("x", 3)
        .attr("dy", ".35em")
        .text(function (d) {
          return d.name;
      });

    // Add the mouse line
    var mouseG = g.append("g")
      .attr("class", "mouse-over-effects");

    mouseG.append("path")
      .attr("class", "mouse-line")
      .style("stroke", "black")
      .style("stroke-width", "1px")
      .style("opacity", "0");

    var lines = document.getElementsByClassName('line');

    var mousePerLine = mouseG.selectAll('.mouse-per-line')
      .data(water_usages)
      .enter()
      .append("g")
      .attr("class", "mouse-per-line");

    mousePerLine.append("circle")
      .attr("r", 7)
      .style("stroke", function (d) {
        return color(d.name);
      })
      .style("fill", "none")
      .style("stroke-width", "2px")
      .style("opacity", "0");

    mousePerLine.append("text")
        .attr("class", "hover-text")
        .attr("dy", "-1em")
        .attr("transform", "translate(10,3)");

    // Append a rect to catch mouse movements on canvas
    mouseG.append('svg:rect')
      .attr('width', width)
      .attr('height', height)
      .attr('fill', 'none')
      .attr('pointer-events', 'all')
      .on('mouseout', function () { // on mouse out hide line, circles and text
        d3.select(".mouse-line")
          .style("opacity", "0");
        d3.selectAll(".mouse-per-line circle")
          .style("opacity", "0");
        d3.selectAll(".mouse-per-line text")
          .style("opacity", "0");
      })
      .on('mouseover', function () { // on mouse in show line, circles and text
        d3.select(".mouse-line")
          .style("opacity", "1");
        d3.selectAll(".mouse-per-line circle")
          .style("opacity", "1");
        d3.selectAll(".mouse-per-line text")
          .style("opacity", "1");
      })
      .on('mousemove', function () { // mouse moving over canvas
        var mouse = d3.mouse(this);

        d3.selectAll(".mouse-per-line")
          .attr("transform", function (d, i) {

            var xDate = x.invert(mouse[0]),
              bisect = d3.bisector(function (d) { return d.date; }).left;
            idx = bisect(d.values, xDate);

            d3.select(this).select('text')
              .text(y.invert(y(d.values[idx].worth)).toFixed(2));

            d3.select(".mouse-line")
              .attr("d", function () {
                var data = "M" + x(d.values[idx].date) + "," + height;
                data += " " + x(d.values[idx].date) + "," + 0;
                return data;
              });
            return "translate(" + x(d.values[idx].date) + "," + y(d.values[idx].worth) + ")";
          });
      });


    };

}
