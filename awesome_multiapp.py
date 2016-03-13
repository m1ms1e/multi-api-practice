from flask import Flask
from flask import render_template
from flask import request
import requests

app = Flask("AwesomeMultiApp")

@app.route("/")
def hello():
	return render_template("awesome-welcome.html")

@app.route("/results", methods=['POST'])

def api_requests():
  
#weather for user's city

  city = request.form['city']

  weather_endpoint = "http://api.openweathermap.org/data/2.5/weather"
  weather_payload = {"q": "London,UK", "units": "metric", "appid": "50586a3fda23cc18fb9d9fadb72b9d7b"}

  weather_response = requests.get(weather_endpoint, params=weather_payload)
  weather_data = weather_response.json()
  temperature = weather_data['main']['temp']

#gif of user's fav animal

  animal = request.form['animal']

  animal_endpoint = "http://api.giphy.com/v1/gifs/search"
  user_animal = {"api_key": "dc6zaTOxFJmzC", "q": animal, "limit": "1"}

  animal_results = requests.get(animal_endpoint, params=user_animal)
  animal_data = animal_results.json()

  picture = animal_data["data"][0]["embed_url"]

#send user simple email

  email = request.form['email']
  name = request.form['name']
  
  requests.post("https://api.mailgun.net/v3/sandbox6e63b31df83c4ef9be4afc85d1d8737f.mailgun.org/messages",
    auth=("api", "key-13154350349d66ca58dc6f9e7065c392"),
    data={"from": "Mimi at AwesomeMultiApp <miriam.keshani@gmail.com>",
      "to": email,
      "subject": "Hello {0}".format(name),
      "html": "<html><h1>Hi {0}!</h1></html><p>Check out this cool gif of your fav animal:{1}</p><br><p>The temperature in {2} is: {3} degC".format(name, picture, city, temperature)})
  return "Check your email"
  #return render_template("awesome-multiapp-results.html", name=name, email=email, link=animal_data["data"][0]["embed_url"])

app.run(	
	debug=True, port=5000
)