
import json,requests
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"



CITY = "valencia"
API_KEY = "49492976e2043731073a4f8ba2ebccc1"
# actualiza la url
URL = BASE_URL + "q=" + CITY + "&appid=" + API_KEY
# hace una peticion HTTP a la url usando la libreria request
response = requests.get(URL)
# comprueba si hay respuesta
errores=0

if response.status_code == 200:
   # obtiene la informacion del archivo json
   data = response.json()

   main = data['main']

   temperature = main['temp']

   humidity = main['humidity']

   pressure = main['pressure']

   report = data['weather']

   ciudad=(f"{CITY}")
   temperatura=(f"{temperature}")
   humedad=""+(f"{humidity}")
   presion=(f"{pressure}")
   tiempo=(f"Tiempo: {report[0]['description']}")
else:
   errores=1
print(humedad)