

async function fetchChartData() {

  symbol  = document.getElementById('stock-symbol').innerText
  console.log(symbol);
  
  var response = await fetch(`/getChartData/${symbol}`);
  var data = await response.json();
  return data;
}


function calculateSMA(data, period) {
  var smaData = [];

  for (var i = period - 1; i < data.length; i++) {
    // console.log(data[i].close);
    var sum = 0;
    for (var j = i - (period - 1); j <= i; j++) {
      sum += parseFloat(data[j].close);
    }
    var average = sum / period;
    smaData.push({ time: data[i].time, value: average });
  }
  // console.log(smaData);
  return smaData;
}

function plotChart(data, smaData) {
  var container = document.getElementById("reportsChart");


  var legend = document.createElement('div');
  legend.className = 'sma-legend';
  container.appendChild(legend);
  legend.style.display = 'block';
  legend.style.left = 3 + 'px';
  legend.style.top = 3 + 'px';

  var chart = LightweightCharts.createChart(container, {
    width: 800,
    height: 500,
    crosshair: {
      mode: LightweightCharts.CrosshairMode.Normal,
    },
    timeScale: {
      timeVisible: true,
    },
  });

  var candleSeries = chart.addCandlestickSeries();
  candleSeries.setData(data);

  var smaLine = chart.addLineSeries({
    color: "rgba(4, 111, 232, 1)",
    lineWidth: 2,
  });
  smaLine.setData(smaData);
}

fetchChartData().then(function(data) {
  var smaData = calculateSMA(data, 20);
  plotChart(data, smaData);
});


// 
// 
// 
// 
