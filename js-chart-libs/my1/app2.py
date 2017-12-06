from flask import Flask, render_template
from datetime import datetime, timedelta
import requests

app = Flask(__name__)

# MULTIPLE POLLUTANTS ON ONE CHART
# Use example of airapp3:
#     series = [{"name": 'PM10', "data": data_dict['pm1']}, {"name": 'PM2.5', "data": data_dict['pm2']},
        # {"name": 'Nitrogen Dioxide', "data": data_dict['no2']}]

# TO DO SEPARATELY: MULTIPLE SITES E.G. PAIRS OF ROADSIDE AND BACKGROUNDS - MY1 AND NKENS
         # interpolated values instead of ''  - use pandas??

site = 'abd'
start = '2017-09-21'
url_list = []
for a in requests.get('http://127.0.0.1:5000/data/pollutants').json().values():
    url_list.append('http://127.0.0.1:5000/data/{0}/{1}/{2}'.format(a, site, start))
print(url_list)


def chart_data(pollutant, site, days):
    start_dt = datetime.today() - timedelta(days=days)
    start = datetime.strftime(start_dt, "%Y-%m-%d")
    url = 'http://127.0.0.1:5000/data/{0}/{1}/{2}'.format(pollutant, site, start)
    # url = 'http://air-aware.com:8083/data/{0}/{1}/{2}'.format(pollutant, site, start)
    data = requests.get(url).json()
    times = [a['time'] for a in data['data']]
    values = []
    for a in data['data']:
        try:
            values.append(int(a['value']))
        except ValueError:
            values.append('')
    return [times, values]


@app.route('/<pollutant>/<site>')
def make_chart(pollutant, site, chartID='chart_ID', chart_type='line', chart_height=550,
               chart_width=800):
    data = chart_data(pollutant, site, days=7)
    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height, "width": chart_width}
    series = [{"name": site, "data": data[1]}]
    # CAN REMOVE NAME FROM SERIES??
    title = {"text": '{} levels at {}'.format(pollutant, site)}
    xAxis = {"title": {"text": 'Time (GMT)'}, "categories": data[0]}
    yAxis = {"title": {"text": 'Concentration (ug/m3)'}}
    return render_template('chart.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis,
                           yAxis=yAxis)


if __name__ == "__main__":
    app.run(host='127.0.0.2')

"""
def get_json(site, days):
    url = get_json_url(site, days)
    resp = requests.get(url)
    data = resp.json()
    array = data['AirQualityData']['Data']
    return array


def get_data(site, days):
    array = get_json(site, days)
    pm1 = [d['@Value'] if d['@Value'] == '' else float(d['@Value']) for d in array if d['@SpeciesCode'] == 'PM10'][
          days * -24:]
    pm2 = [d['@Value'] if d['@Value'] == '' else float(d['@Value']) for d in array if d['@SpeciesCode'] == 'FINE'][
          days * -24:]
    no2 = [d['@Value'] if d['@Value'] == '' else float(d['@Value']) for d in array if d['@SpeciesCode'] == 'NO2'][
          days * -24:]
    hours = list(map(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S").strftime('%H:%M'), ([d['@MeasurementDateGMT']
                 for d in array])))
    return dict(pm1=pm1, pm2=pm2, no2=no2, hours=hours)


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
