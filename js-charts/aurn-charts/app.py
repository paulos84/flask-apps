from flask import Flask, render_template
import requests

app = Flask(__name__)

def chart_data(site, days, p1, p2):
    url = 'http://www.air-aware.com:8083/data/{0}/{1}'.format(site, days)
    resp = requests.get(url).json()
    data = resp[site.upper()]['latest_data']
    times = [a['time'] for a in data]
    s1 = ['' if a['values'][p1] in ['n/a', 'n/m'] else int(a['values'][p1]) for a in data]
    s2 = ['' if a['values'][p2] in ['n/a', 'n/m'] else int(a['values'][p2]) for a in data]
    return {'times': times, 's1': s1, 's2': s2, 'site_name': resp[site.upper()]['info']['name']}

@app.route('<site>/<int:days>/<pollutant_1>/<pollutant_2>')
def make_chart(site, days, pollutant_1, pollutant_2, chartID='chart_ID', chart_type='line', chart_height=550,
               chart_width=800):
    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height, "width": chart_width}
    data = chart_data(site, days, pollutant_1,  pollutant_2)
    series = [{"name": pollutant_1, "data": data['s1']}, {"name": pollutant_2, "data": data['s2']}]
    title = {"text": 'Recent air pollution levels at {}'.format(data['site_name'])}
    xAxis = {"categories": data['times']}
    yAxis = {"title": {"text": 'Concentration (ug/m-3)'}}
    return render_template('chart.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis,
                           yAxis=yAxis)

if __name__ == "__main__":
    app.run(host='127.0.0.2')
