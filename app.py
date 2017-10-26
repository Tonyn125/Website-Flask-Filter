import csv
from lxml import etree
from flask import Flask, render_template, request
import aggregate_calc
app = Flask(__name__, static_folder='.', static_url_path='')

def make_table():
	start = '<script type="text/javascript">google.charts.load("current", {"packages":["table"]});google.charts.setOnLoadCallback(drawTable);function drawTable() {var data = new google.visualization.DataTable();'
	end = 	'var table = new google.visualization.Table(document.getElementById("table_div"));table.draw(data, {showRowNumber: false, width: "100%", height: "100%", page: "enable", pageSize: "25", pageButtons: "both"});}</script><div id="table_div"></div>'
	fp = open("datar.csv")
	data = csv.reader(fp)
	col = ''
	header = next(data)
	help = 'data.addRows(['
	help2 = ']);'
	for i in header:
		col += 'data.addColumn("number","'+ i +'");' 
	for i in data:
		help += '['
		for u in i:
			help += '{v:'+u+', f: "'+ u +'"},' 
		help += '],'
	return start+ col + help + help2 + end#+ add + adde + end

def there(agg, y, x, fil):
	piv = aggregate_calc.calc_agg(int(agg), int(y), int(x), int(fil))
	strpiv = '<table id="g1t", border = "2"><tr><td></td>'

	fp = open('zone.csv')
	labels = csv.reader(fp)
	for i in range(int(y) + 1):
		row_lbl = next(labels)
	fp2 = open('head.csv')
	header = csv.reader(fp2)
	if int(x) < 6:
		for i in range(int(x) - 2):
			col_lbl = next(header)
	elif int(x) > 5 and int(x) < 9:
		if int(x) == 6 or int(x) == 8:
			col_lbl = [i for i in range(16)]
		else:
			col_lbl = [i for i in range(11)]
	else:
		for i in range(int(x) - 5):
			col_lbl = next(header)
	for head in col_lbl:
		strpiv += '<td>' + str(head) + '</td>'

	count = 0
	for row in piv:
		strpiv += '<tr><td>' + str(row_lbl[count]) + '</td>'
		for data in row:
			strpiv += '<td>' + str(data) + '</td>'
		strpiv += '</tr>'
		count += 1
	strpiv += '</table>'

	return str(strpiv)

@app.route('/')
def index():
	return render_template("home.html")+render_template("footer.html")

@app.route('/tabledata')
def data():
	return render_template("data.html") + make_table() +render_template("footer.html")
	
@app.route('/p_table')
def pivot():
	return render_template("p_table.html") + render_template("footer.html")
	
@app.route('/', methods=['POST'])
def my_form_post():
	
	xaxis_ = request.form['text1']
	filter_ = request.form['text2']
	yaxis_ = request.form['text3']
	agg_met = request.form['text4']
	#strpiv_ = there(agg_met, yaxis_, xaxis_, filter_)
	#open('agg.csv', 'w').write(strpiv_)

	return render_template("p_table2.html") + there(agg_met, yaxis_, xaxis_, filter_) + render_template("footer.html")
	
@app.route('/visuals')
def vis():
	return render_template("visuals.html") + render_template("footer.html")
	
@app.route('/observations')
def about():
	return render_template("observations.html") + render_template("footer.html")

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=3001)