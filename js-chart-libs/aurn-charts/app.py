from flask import Flask, render_template
import requests


app = Flask(__name__)

# TO DO - make interpolated values instead of '', multiple sites (e.g. MY1, NKENS)
    # 2 sites and multiple pollutants


def chart_data(site, days, poll_1,  poll_2):
    url = 'http://www.air-aware.com:8083/data/{0}/{1}'.format(site, days)
    resp = requests.get(url).json()
    data = resp['MY1']['latest_data']
    times = [a['time'] for a in data]
    series_1 = ['' if a['values'][poll_1] in ['n/a', 'n/m'] else int(a['values'][poll_1]) for a in data]
    series_2 = ['' if a['values'][poll_2] in ['n/a', 'n/m'] else int(a['values'][poll_2]) for a in data]
    return [times, series_1, series_2]


@app.route('/<pollutant>/<site>/<int:days>')
def make_chart(pollutant, site, days, chartID='chart_ID', chart_type='line', chart_height=550,
               chart_width=800):
    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height, "width": chart_width}
    data = chart_data(pollutant, site, days)
    series = [{"name": 'gjh', "data": data[1]}]
    # CAN REMOVE NAME FROM SERIES??
    title = {"text": '{} levels at {}'.format(pollutant, site)}
    xAxis = {"title": {"text": 'Time (GMT)'}, "categories": [1,2,3,4]}
    # "categories": data[0]}
    yAxis = {"title": {"text": 'Concentration (ug/m-3)'}}
    return render_template('chart.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis,
                           yAxis=yAxis)


if __name__ == "__main__":
    app.run(host='127.0.0.2')
