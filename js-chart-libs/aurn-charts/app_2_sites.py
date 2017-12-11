from flask import Flask, render_template
import requests

app = Flask(__name__)

def chart_data(site, days, *args, site2=None):
    if site2:
        url = 'http://www.air-aware.com:8083/data/{0}/{1}/{2}'.format(site, site2, days)
    else:
        url = 'http://www.air-aware.com:8083/data/{0}/{1}'.format(site, days)
    resp = requests.get(url).json()
    data = resp[site.upper()]['latest_data']
    times = [a['time'] for a in data]
    s1 = ['' if a['values'][args[0]] in ['n/a', 'n/m'] else int(a['values'][args[0]]) for a in data]
    try:
        s2 = ['' if a['values'][args[1]] in ['n/a', 'n/m'] else int(a['values'][args[1]]) for a in data]
    except IndexError:
        s2 = None
    return {'times': times, 's1': s1, 's2': s2}

@app.route('<site>/<int:days>/<pollutant_1>/<pollutant_2>')
def make_chart(site, days, pollutant_1, pollutant_2=None, chartID='chart_ID', chart_type='line', chart_height=550,
               chart_width=800):
    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height, "width": chart_width}
    data = chart_data(site, days, pollutant_1,  pollutant_2)
    series = [{"name": pollutant_1, "data": data['s1']}, {"name": pollutant_2, "data": data['s2']}]
    title = {"text": 'Recent air pollution levels at {}'.format(site)}
    xAxis = {"title": {"text": 'Time (GMT)'}, "categories": data['times']}
    yAxis = {"title": {"text": 'Concentration (ug/m-3)'}}
    return render_template('chart.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis,
                           yAxis=yAxis)

@app.route('two_sites/<site_1>/<site_2>/<int:days>/<pollutant_1>/<pollutant_2>')
def plot_two_sites(site_1, site_2, days, pollutant_1, pollutant_2=None, chartID='chart_ID', chart_type='line',
                   chart_height=550, chart_width=800):
    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height, "width": chart_width}
    data_1 = chart_data(site_1, days, pollutant_1, pollutant_2)
    data_2 = chart_data(site_2, days, pollutant_1, pollutant_2)
    dict_list = [{"name": pollutant_1 + 'at' + site_1, "data": data_1['s1']},
                 {"name": pollutant_2 + 'at' + site_1, "data": data_1['s2']},
                 {"name": pollutant_1 + 'at' + site_2, "data": data_2['s1']},
                 {"name": pollutant_2 + 'at' + site_2, "data": data_2['s2']}]
    series = [a for a in dict_list if a['data']]
    title = {"text": 'Recent air pollution levels at {} and {}'.format(site_1, site_2)}
    xAxis = {"title": {"text": 'Time (GMT)'}, "categories": data_1['times']}
    yAxis = {"title": {"text": 'Concentration (ug/m-3)'}}
    return render_template('chart.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis,
                           yAxis=yAxis)


if __name__ == "__main__":
    app.run(host='127.0.0.2')

"""
To do: mention debugging of plotting using logging to check what values are passed to the Jinja2 template
a = 'Look'
b = 'leap!'
c = [2]

logging.basicConfig(filename='myapp.log', level=logging.INFO)
logging.info('%s before you %s', a, b)
logging.info( '%s', c)
"""