//var chart = $('.graph');
//
//var shower_data = {
//    x: [],
//    y: [],
//    type: 'scatter'
//};
//var toilet_data = {
//    x: [],
//    y: [],
//    type: 'scatter'
//};
//var bathroom_sink_data = {
//    x: [],
//    y: [],
//    type: 'scatter'
//};
//var kitchen_sink_data = {
//    x: [],
//    y: [],
//    type: 'scatter'
//};
//var drinking_water_data = {
//    x: [],
//    y: [],
//    type: 'scatter'
//};
//var sprinkler_data = {
//    x: [],
//    y: [],
//    type: 'scatter'
//};
//var miscellaneous_data = {
//    x: [],
//    y: [],
//    type: 'scatter'
//};
//var date_data = {};
//
//var layout = {
//  title:'A Line Chart in Plotly'
//};
//
//
//var graph_data = [shower_data, toilet_data, bathroom_sink_data, kitchen_sink_data, drinking_water_data,
//                    sprinkler_data, miscellaneous_data];
//
//Plotly.plot(chart, graph_data, {});


var speedCanvas = document.getElementById("speedChart");

Chart.defaults.global.defaultFontFamily = "Lato";
Chart.defaults.global.defaultFontSize = 18;

var speedData = {
  labels: ["0s", "10s", "20s", "30s", "40s", "50s", "60s"],
  datasets: [{
    label: "Car Speed (mph)",
    data: [0, 59, 75, 20, 20, 55, 40],
  }]
};

var chartOptions = {
  legend: {
    display: true,
    position: 'top',
    labels: {
      boxWidth: 80,
      fontColor: 'black'
    }
  }
};

var lineChart = new Chart(speedCanvas, {
  type: 'line',
  data: speedData,
  options: chartOptions
});