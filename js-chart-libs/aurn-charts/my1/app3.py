from flask import Flask, render_template
from datetime import datetime, timedelta
import requests

app = Flask(__name__)

def get_data(pollutant, site_code, days):
    start_dt = datetime.today() - timedelta(days=days)
    start = datetime.strftime(start_dt, "%Y-%m-%d")
    end = datetime.strftime(datetime.today() - timedelta(days=1), "%Y-%m-%d")
    url = 'http://air-aware.com:8083/data/{0}/{1}/{2}/{3}'.format(pollutant, site_code, start, end)
    data = requests.get(url).json()
    return data

#TO DO - make interpolated values instead of ''  - use list comp within make_chart()
def clean_data(data):
    clean = []
    for a in data.values():
        try:
            clean.append(float(a))
        except ValueError:
            clean.append('')
    return clean


@app.route('/chart/')
@app.route('/chart/<pollutant>/<site_code>/<int:days>')
def make_chart(pollutant='PM10', site_code='ABD', days=5, chartID='chart_ID', chart_type='line', chart_height=550,
               chart_width=800):
    recent_data = get_data(pollutant,  site_code, days)
    data = ['' if a in ['n/a', 'n/m'] else int(a) for a in recent_data.values()]
    times = [a for a in recent_data.keys()]
    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height, "width": chart_width}
    series = [{"name": 'Store 1', "data": data}]
    title = {"text": 'Monthly Sales'}
    xAxis = {"title": {"text": 'Product Model'}, "categories": times}
    yAxis = {"title": {"text": 'Turnover ($)'}}
    return render_template('chart.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis,
                           yAxis=yAxis)

"""
@app.route('/chart/<pollutant>/<site_code>/<int:days>')
def make_chart(pollutant, site_code, days, chartID='chart_ID', chart_type='line', chart_height=550, chart_width=800):
    recent_data = get_data(pollutant, site_code, days)
    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height, "width": chart_width}
    series = [{"name": 'NO2', "data": [a for a in recent_data.values()]}]
    title = {"text": 'Nitrogen Dioxide and PM10 Measurements'}
    xaxis = {"categories": [a for a in recent_data.keys()]}
    yaxis = {"title": {"text": 'Concentration (ug/m3)'}}
    return render_template('chart.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xaxis, yAxis=yaxis)
"""

if __name__ == "__main__":
    app.run()

"""
@app.route('/chart/<site><int:days>')
def make_chart(site='MY1', days=1, chartID='chart_ID', chart_type='line', chart_height=550, chart_width=800):
    data_dict = get_data(site, days)
    metadata_dict = get_metadata(site)
    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height, "width": chart_width}
    series = [{"name": 'PM10', "data": data_dict['pm1']}, {"name": 'PM2.5', "data": data_dict['pm2']},
              {"name": 'Nitrogen Dioxide', "data": data_dict['no2']}]
    title = {"text": 'Recent air pollution levels:   ' + (custom_strftime('%B {S}, %Y', datetime.now()))}
    xaxis = {"categories": data_dict['hours'][days * -24:]}
    yaxis = {"title": {"text": 'Concentration (ug/m3)'}}
    return render_template('detail.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xaxis, yAxis=yaxis)
    """
