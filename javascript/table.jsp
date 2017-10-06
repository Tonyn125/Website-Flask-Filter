//IF YOU WANT TO PLACE INTO SITE, PLACE ALL THIS CODE INTO <SCRIPT> here </SCRIPT>
//	<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script> PUT THIS INTO HEADER LIKE ON DATA.HTML
// IT WILL OUTPUT INTO THIS >>>>>><div id="table_div"></div>
//CHECK make_table() CODE IN APP.PY to see generation
//https://developers.google.com/chart/interactive/docs/gallery/table#example ORIGINAL GRAPH 
	google.charts.load('current', {'packages':['table']});
	google.charts.setOnLoadCallback(drawTable);

	function drawTable() {
		var data = new google.visualization.DataTable();

	//REMOVE THIS AFTER
	//PLACE COLUMN NAMES HERE
	//EXAMPLE
		data.addColumn('string', 'Name');
        data.addColumn('number', 'Salary');
        data.addColumn('boolean', 'Full Time Employee');
	
	
	//REMOVE THIS AFTER
	//PLACE ROWS HERE
	//EXAMPLE
		data.addRows([
          ['Mike',  {v: 10000, f: '$10,000'}, true],
          ['Jim',   {v:8000,   f: '$8,000'},  false],
          ['Alice', {v: 12500, f: '$12,500'}, true],
          ['Bob',   {v: 7000,  f: '$7,000'},  true]
        ]);
		
		
	var table = new google.visualization.Table(document.getElementById("table_div"));
	table.draw(data, {showRowNumber: true, width: "100%", height: "100%", page: "enable", pageSize: '25', pageButtons: 'both'});
	}