var chart = LightweightCharts.createChart(document.getElementById('reportsChart'), {
	width: 800,
	height: 500,
	crosshair: {
	  mode: LightweightCharts.CrosshairMode.Normal,
	},
  });
  
  var candleSeries = chart.addCandlestickSeries();


  function plotData(count) {
	if (count <= data.length) {
	  for (var i = currentIndex; i < count; i++) {
		candleSeries.update(data[i]);
		currentIndex++;
	  }
	  plottedDataCount = count;
	}
  }
 

  
  var currentIndex = 0;
  var data = [];

  
  function fetchData() {
	fetch('/getChartData/SBIN.NS')
	  .then(function(response) {
		return response.json();
	  })
	  .then(function(jsonData) {
		data = jsonData;
		var initialDataCount = Math.floor(data.length * 0.9);
		plotData(initialDataCount);
		plotNextData();
	  })
	  .catch(function(error) {
		console.log('Error fetching chart data:', error);
	  });
  }
  
  function plotNextData() {
	  if (currentIndex < data.length) {
		//   console.log(data[currentIndex])
			  document.getElementById('dynamic-data-price').innerHTML = `<span class="fw-bold fs-4  ${(data[currentIndex].close >= data[currentIndex].open) ? "text-success" : "text-danger"} ">
			  
			  ${parseFloat(data[currentIndex].close).toFixed(2)} </span>`

	  candleSeries.update(data[currentIndex]);
	  currentIndex++;
	}
  }
  
  fetchData();
  setInterval(fetchData, 60000); // Fetch data every minute
  
  setInterval(plotNextData, 2000);
