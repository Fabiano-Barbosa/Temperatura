from flask import Flask, render_template, request, json
import os.path
import requests
import datetime

app = Flask(__name__)

@app.route('/previsao', methods=['POST'])
def previsao():
        keyapi = '218a0ba28309d82d71363d7e9f878d33'
        cidade   = request.form['cidade']
        agora    = requests.get('http://api.openweathermap.org/data/2.5/weather?q='+cidade+',BR&appid='+keyapi)
        previsao = requests.get('http://api.openweathermap.org/data/2.5/forecast?q='+cidade+',BR&appid='+keyapi)

        json_agora = agora.json()

        if(int(json_agora['cod'])==404):
          return render_template('404.html')
        else:
          #Informações sobre o local
          res_pais     = str(json_agora['sys']['country'])
          res_cidade   = str(json_agora['name'])
          res_lat      = float(json_agora['coord']['lat'])
          res_long     = float(json_agora['coord']['lon'])

          #Informação sobre o tempo Agora
          temp_kelvin  = float(json_agora['main']['temp'])
          agora_temp   = round((temp_kelvin - 273.15),1)
          temp_kelvin  = float(json_agora['main']['feels_like'])
          agora_sens= round((temp_kelvin - 273.15),1)
          temp_kelvin  = float(json_agora['main']['temp_min'])
          agora_min = round((temp_kelvin - 273.15),1)
          temp_kelvin  = float(json_agora['main']['temp_max'])
          agora_max = round((temp_kelvin - 273.15),1)

          #Informação sobre a previsao
          prev_c = []
          prev_h = []
          json_prev    = previsao.json()
          for i in range(0,12,+2):
            temp_k  = [float(json_prev['list'][i]['main']['temp_min']), float(json_prev['list'][i]['main']['temp_max'])]
            prev_c.append( [round((temp_k[0] - 273.15),1), round((temp_k[1] - 273.15),1)] )
            prev_h.append ( datetime.datetime.fromtimestamp( int(json_prev['list'][i]['dt']) ).strftime('%d/%m/%Y %H:%M') )

          log = {}
          log['consulta'] = []
          log['consulta'].append({
                  'hora': datetime.datetime.now().strftime('%d/%m/%Y %H:%M'),
                  'ip': request.environ['REMOTE_ADDR'],
                  'pais': res_pais,
                  'cidade': res_cidade,
                  'lat': res_lat,
                  'long': res_long,
                  'agora_temp': agora_temp,
                  'agora_sens': agora_sens,
                  'agora_min': agora_min,
                  'agora_max': agora_max
          })
            
          with open('log.txt', 'a') as arq:
            json.dump(log, arq, ensure_ascii=False, indent=4
                      )
          return render_template('previsao.html',
                                 temp1=agora_temp, sens1=agora_sens,
                                 local_pais=res_pais, local_cidade=res_cidade, latitude=res_lat, longitude=res_long,
                                 prev_hora_0=prev_h[0], prev_0_1=prev_c[0][0], prev_0_2=prev_c[0][1],
                                 prev_hora_1=prev_h[1], prev_1_1=prev_c[1][0], prev_1_2=prev_c[1][1],
                                 prev_hora_2=prev_h[2], prev_2_1=prev_c[2][0], prev_2_2=prev_c[2][1],
                                 prev_hora_4=prev_h[4], prev_4_1=prev_c[4][0], prev_4_2=prev_c[4][1],
                                 prev_hora_3=prev_h[3], prev_3_1=prev_c[3][0], prev_3_2=prev_c[3][1]
                                 )

@app.route('/log', methods=['GET'])
def log():

        if(os.path.isfile('log.txt')):
          log_file = open('log.txt', 'r').read()
        else:
          log_file = 'Sem consultas'

        return render_template('log.html',
                log=log_file
                )
	
@app.route('/')
def index():
	return render_template('index.html')

if __name__ == '__main__':
	app.run(debug=True)




