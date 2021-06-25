from flask import Flask, jsonify, request, render_template
import random

import requests 
import json


app = Flask( 
	__name__,
	template_folder='./templates',  
	static_folder='static' 
)
  
@app.route('/')
def home():
  return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/nasa')
def mars():
  response = requests.get("https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&api_key=faRn6vfvjvAmibI3UeuCfdYb3S4BFBP7rAPSfsu2")

  python_dict = json.loads(response.content)
  url_pic = python_dict['photos'][0]['img_src']
  name = python_dict['photos'][0]['camera']['full_name']
  photo_id = python_dict['photos'][0]['id']

  return render_template('nasa.html', img_url = url_pic, name = name,photo_id = photo_id)

@app.route('/catfacts')
def catfacts():
  response = requests.get("https://cat-fact.herokuapp.com/facts")

  python_list = json.loads(response.content)

  all_cat_facts = []

  for each in python_list:
    all_cat_facts.append(each['text'])
  all_cat_facts.pop(2)

  return render_template('catfacts.html',all_cat_facts = all_cat_facts)

@app.route('/dogfacts')
def dogfacts():

  num_facts = 20
  request_url = f'https://dog-facts-api.herokuapp.com/api/v1/resources/dogs?number={num_facts}'
  response = requests.get(request_url)
  python_list = json.loads(response.content)

  all_dog_facts = []

  for each in python_list:
    all_dog_facts.append(each['fact'])
  
  return render_template('dogfacts.html',all_dog_facts = all_dog_facts)

@app.route('/httpcats')
def httpcats():

  status_codes = [100,200,202, 204,300, 302,400, 401, 402, 403, 404, 405, 406, 418, 500, 501]
  request_urls = []
  for each_code in status_codes:
    request_urls.append(f'https://http.cat/{each_code}')

  return render_template('httpcats.html',request_urls = request_urls)

@app.route('/animequotes')
def animequotes():

  request_url = "https://animechan.vercel.app/api/quotes"
  
  response = requests.get(request_url)
  python_list = json.loads(response.content)

  all_data = []
  for each in python_list:
    all_data.append({"anime":each['anime'],"character":each['character'],"quote": each['quote']})

  return render_template('animequotes.html',all_data = all_data)

@app.route('/urlscan')
def urlscan():

  api_key = '79a42f7a-b223-468b-8247-bf19e2165d14'
  url = "https://web.mit.edu/"

  #Submission 
  headers = {'API-Key':api_key,'Content-Type':'application/json'}
  data = {"url": url, "visibility": "public"}
  requests.post('https://urlscan.io/api/v1/scan/',headers=headers, data=json.dumps(data))
  uuid = "663a6001-8448-4368-b150-bff014d3c4a0"

  #Result
  submission_response = requests.get(f'https://urlscan.io/api/v1/result/{uuid}')
  python_dict = json.loads(submission_response.content)

  malicious = python_dict["verdicts"]["overall"]["malicious"]
  
  verdict = "Not Malicious"
  if malicious:
    verdict = "Malicious"
  
  return render_template('urlscan.html',python_dict = python_dict, verdict = verdict)

@app.route('/MET')
def met():

  request_url = "https://collectionapi.metmuseum.org/public/collection/v1/objects"

  response = requests.get(request_url)
  python_dict = json.loads(response.content)

  all_object_ids = python_dict["objectIDs"]
  all_object_ids = all_object_ids[50:52]


  object_request_urls = []

  for each in all_object_ids:
    object_request_urls.append(f'https://collectionapi.metmuseum.org/public/collection/v1/objects/{each}')
  
  all_data = []

  for each_request in object_request_urls:
    all_data.append(json.loads(requests.get(each_request).content))

  return render_template('books.html',all_data = all_data)

@app.route('/books')
def books():

  ids = ["OL23204W","OL3871697W"]
  request_urls = []

  for each in ids:
    request_urls.append(f'https://openlibrary.org/works/{each}.json')
  
  all_data = []

  for each_request in request_urls:
    all_data.append(json.loads(requests.get(each_request).content))

  return render_template('books.html',all_data = all_data)

@app.route('/bankholidays')
def bankholidays():

  request_url = "https://www.gov.uk/bank-holidays.json"

  all_data = json.loads(requests.get(request_url).content)

  england_wales = all_data["england-and-wales"]["events"]
  england_wales_holidays = set()
  for each in england_wales:
    england_wales_holidays.add(each["title"])
  
  scotland = all_data["scotland"]["events"]
  scotland_holidays = set()
  for each in scotland:
    scotland_holidays.add(each["title"])

  northern_ireland = all_data["northern-ireland"]["events"]
  northern_ireland_holidays = set()
  for each in northern_ireland:
    northern_ireland_holidays.add(each["title"])

  return render_template('bankholidays.html',england_wales_holidays = england_wales_holidays, scotland_holidays = scotland_holidays,northern_ireland_holidays = northern_ireland_holidays)

@app.route('/bitcoin')
def bitcoin():

  request_url = "http://api.bitcoincharts.com/v1/weighted_prices.json"

  all_data = json.loads(requests.get(request_url).content)
  del all_data["timestamp"]
  return render_template('bitcoin.html',all_data = all_data)

@app.route('/wallstreetbets')
def wallstreetbets():

  request_url = "https://dashboard.nbshare.io/api/v1/apps/reddit"

  all_data = json.loads(requests.get(request_url).content)

  return render_template('wallstreetbets.html',all_data = all_data)

@app.route('/currencies')
def currencies():

  currency = "usd"
  request_url = f'https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/{currency}.json'

  all_data = json.loads(requests.get(request_url).content)

  return render_template('currencies.html',all_data = all_data, currency = currency)

@app.route('/profanitycheck')
def profanitycheck():

  text = "profanitycheckgoddamn"

  request_url = f'https://www.purgomalum.com/service/containsprofanity?text={text}'
  data = json.loads(requests.get(request_url).content)

  if data == True:
    profanity = "Contains Profanity"
  else:
    profanity = "Does Not Contain Profanity"

  return render_template('profanitycheck.html',profanity = profanity, text = text)

@app.route('/agecheck')
def agecheck():

  name = "ashar"

  request_url = f'https://api.agify.io?name={name}'
  data = json.loads(requests.get(request_url).content)

  return render_template('agecheck.html',data = data, name = name)

@app.route('/bored')
def bored():

  activities_data = []
  num_of_activities = 4
  request_url = "http://www.boredapi.com/api/activity/"

  for i in range(num_of_activities):
    activities_data.append(json.loads(requests.get(request_url).content))

  return render_template('bored.html',activities_data = activities_data)

@app.route('/genderize')
def genderize():

  name = "ashar"

  request_url = f'https://api.genderize.io?name={name}'
  data = json.loads(requests.get(request_url).content)

  return render_template('genderize.html',data = data, name = name)

@app.route('/nationalize')
def nationalize():

  name = "austin"

  request_url = f'https://api.nationalize.io?name={name}'
  data = json.loads(requests.get(request_url).content)

  return render_template('nationalize.html',data = data, name = name)

@app.route('/githubtrending')
def githubtrending():

  request_url = "https://api.trending-github.com/github/spoken-languages"
  data = json.loads(requests.get(request_url).content)

  return render_template('githubtrending.html',data = data)

@app.route('/carbonintensity')
def carbonintensity():

  request_url = "https://api.carbonintensity.org.uk/intensity"

  data = json.loads(requests.get(request_url).content)

  return render_template('carbonintensity.html',data = data)

@app.route('/inspirequotes')
def inspirequotes():

  request_url = "https://api.fisenko.net/quotes"
  num_quotes = 4

  all_data = []

  for i in range(num_quotes):
    all_data.append(json.loads(requests.get(request_url).content))

  return render_template('inspirequotes.html',all_data = all_data)

@app.route('/favicon.ico')
def favicon():

  return render_template('favicon.html')

if __name__ == "__main__":  # Makes sure this is the main process
	app.run( # Starts the site
		host='0.0.0.0',  # EStablishes the host, required for repl to detect the site
		port=random.randint(2000, 9000),  # Randomly select the port the machine hosts on.
    debug=True
	)