from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/chart')
def index(chartID='chart_ID', chart_type='bar', chart_height=350):
    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height, }
    series = [{"name": 'Store 1', "data": [8, 22, 15]}, {"name": 'Store 2', "data": [14, 17, 9]}]
    title = {"text": 'December 2018 Sales'}
    xAxis = {"categories": ['A', 'B', 'C']}
    yAxis = {"title": {"text": 'Product Model'}}
    return render_template('chart.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis,
                           yAxis=yAxis)

if __name__ == "__main__":
    app.run()
