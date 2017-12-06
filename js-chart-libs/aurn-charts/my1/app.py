from flask import Flask, render_template
from datetime import datetime, timedelta
import requests
import logging

app = Flask(__name__)


a = 'Look'
b = 'leap!'
c = [2]

logging.basicConfig(filename='myapp.log', level=logging.INFO)
logging.info('%s before you %s', a, b)
logging.info( '%s', c)


def chart_data(pollutant, site, days):
    start_dt = datetime.today() - timedelta(days=days)
    start = datetime.strftime(start_dt, "%Y-%m-%d")
    url = 'http://127.0.0.1:5000/data/{0}/{1}/{2}'.format(pollutant, site, start)
    # url = 'http://air-aware.com:8083/data/{0}/{1}/{2}'.format(pollutant, site, start)
    data = requests.get(url).json()
    times = [a['time'] for a in data['data']]
    values = ['' if a['value'] in ['n/a', 'n/m'] else int(a['value']) for a in data['data']]
    return [times, values]



# refactor (part 2?) more robust as int(a...) could throw ValueError: invalid literal for int() with base 10
#  -use test_data to check that works
# TO DO - make interpolated values instead of '', multiple sites (e.g. MY1, NKENS)



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

"""
def chart_data(pollutant, site):
    #start_dt = datetime.today() - timedelta(days=days)
    #start = datetime.strftime(start_dt, "%Y-%m-%d")
    #url = 'http://127.0.0.1:5000/data/{0}/{1}/{2}'.format(pollutant, site, start)
    url = 'http://air-aware.com:8083/data/{0}/{1}/2017-10-08/2017-10-10'.format(pollutant, site)
    #data = requests.get(url).json()
    #times = [a['time'] for a in data['data']]
    #values = ['' if a['value'] in ['n/a', 'n/m'] else int(a['value']) for a in data['data']]
    #return [times, values]
    data = requests.get(url).json().values()
    return [6 if a == 'n/a' else int(a) for a in data]


def chart_data(pollutant, site, days):
    start_dt = datetime.today() - timedelta(days=days)
    start = datetime.strftime(start_dt, "%Y-%m-%d")
    url = 'http://127.0.0.1:5000/data/{0}/{1}/{2}'.format(pollutant, site, start)
    # url = 'http://air-aware.com:8083/data/{0}/{1}/{2}'.format(pollutant, site, start)
    data = requests.get(url).json()
    times = [a['time'] for a in data['data']]
    values = ['' if a['value'] in ['n/a', 'n/m'] else int(a['value']) for a in data['data']]
    return [times, values]


@app.route('/')
# @app.route('/<pollutant>/<site>')
def make_chart(chartID='chart_ID', chart_type='line', chart_height=550,
               chart_width=800):
    data = chart_data('no2', 'abd', 27)
    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height, "width": chart_width}
    series = [{"name": 'abd', "data": data[1]}]
    # CAN REMOVE NAME FROM SERIES??
    title = {"text": '{} levels at {}'.format('pm25', 'abd')}
    xAxis = {"title": {"text": 'Time (GMT)'}, "categories": [1,2,3,4]}
    #"categories": data[0]
    yAxis = {"title": {"text": 'Concentration (ug/m-3)'}}
    return render_template('chart.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis,
                           yAxis=yAxis)
                           """