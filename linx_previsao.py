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
          for i in range(0,40,+2):
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
                                 prev_hora_3=prev_h[3], prev_3_1=prev_c[3][0], prev_3_2=prev_c[3][1],

                                 prev_hora_4=prev_h[4], prev_4_1=prev_c[4][0], prev_4_2=prev_c[4][1],
                                 prev_hora_5=prev_h[5], prev_5_1=prev_c[5][0], prev_5_2=prev_c[5][1],
                                 prev_hora_6=prev_h[6], prev_6_1=prev_c[6][0], prev_6_2=prev_c[6][1],
                                 prev_hora_7=prev_h[7], prev_7_1=prev_c[7][0], prev_7_2=prev_c[7][1],

                                 prev_hora_8=prev_h[8], prev_8_1=prev_c[8][0], prev_8_2=prev_c[8][1],
                                 prev_hora_9=prev_h[9], prev_9_1=prev_c[9][0], prev_9_2=prev_c[9][1],
                                 prev_hora_10=prev_h[10], prev_10_1=prev_c[10][0], prev_10_2=prev_c[10][1],
                                 prev_hora_11=prev_h[11], prev_11_1=prev_c[11][0], prev_11_2=prev_c[11][1],

                                 prev_hora_12=prev_h[12], prev_12_1=prev_c[12][0], prev_12_2=prev_c[12][1],
                                 prev_hora_13=prev_h[13], prev_13_1=prev_c[13][0], prev_13_2=prev_c[13][1],
                                 prev_hora_14=prev_h[14], prev_14_1=prev_c[14][0], prev_14_2=prev_c[14][1],
                                 prev_hora_15=prev_h[15], prev_15_1=prev_c[15][0], prev_15_2=prev_c[15][1],

                                 prev_hora_16=prev_h[16], prev_16_1=prev_c[16][0], prev_16_2=prev_c[16][1],
                                 prev_hora_17=prev_h[17], prev_17_1=prev_c[17][0], prev_17_2=prev_c[17][1],
                                 prev_hora_18=prev_h[18], prev_18_1=prev_c[18][0], prev_18_2=prev_c[18][1],
                                 prev_hora_19=prev_h[19], prev_19_1=prev_c[19][0], prev_19_2=prev_c[19][1]
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




