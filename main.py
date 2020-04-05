from flask import Flask, url_for, render_template, request, redirect
from decouple import config as config_decouple
import requests


app = Flask(__name__)
#from decouple import config







@app.route('/prueba')
def index():
	info = requests.get('https://rickandmortyapi.com/api/episode/')
	dicc = info.json()
	numero_paginas = dicc["info"]["pages"]
	lista_completa = [dicc]
	lista_episodios = []
	for episode_dic in dicc["results"]:
			nombre_episodio = episode_dic
			lista_episodios.append(nombre_episodio)
	for i in range(numero_paginas - 1):
		next_pagina = dicc["info"]["next"]
		info_nueva = requests.get(next_pagina)
		dicc = info_nueva.json()
		for episode_dic in dicc["results"]:
			nombre_episodio = episode_dic
			lista_episodios.append(nombre_episodio)

		lista_completa.append(dicc)
	return str(lista_episodios)



@app.route('/')
def episodes():
	info = requests.get('https://rickandmortyapi.com/api/episode/')
	dicc = info.json()
	numero_paginas = dicc["info"]["pages"]
	lista_completa = [dicc]
	lista_episodios = []
	for episode_dic in dicc["results"]:
		lista_episodios.append(episode_dic)
	for i in range(numero_paginas - 1):
		next_pagina = dicc["info"]["next"]
		info_nueva = requests.get(next_pagina)
		dicc = info_nueva.json()
		for episode_dic in dicc["results"]:
			lista_episodios.append(episode_dic)

		lista_completa.append(dicc)
	
	return render_template('episodes.html', episodes=lista_episodios)


@app.route('/', methods=['POST'])
def episodes_busqueda():
	texto = request.form['text']
	return texto.upper()

@app.route('/episode/<string:argu>', methods=['GET', 'POST'])
def episode_route(argu):
	info = requests.get('https://rickandmortyapi.com/api/episode/'+ argu)
	dicc = info.json()
	characters = dicc["characters"]
	name = dicc["name"]
	codigo = dicc["episode"]
	#lista_info = [name, codigo]
	characters_objects = []
	#for character_url in characters:
		#character_object = requests.get(character_url)
		#dicc_character = character_object.json()
		#characters_objects.append(dicc_character)
	lista_id_characters = []
	for character_url in characters:
		lista_id_characters.append(id_url_character(character_url))
	print(f"la lista es {lista_id_characters}")
	characters_dicc = requests.get('https://rickandmortyapi.com/api/character/'+ str(lista_id_characters)).json()

	lista_info = [name, codigo, characters_dicc]

    #lista_info = [name, codigo]
	#dicc = info.json()
	
	return render_template('episode.html', episode_lista=lista_info)


@app.route('/character/<string:id>', methods=['GET', 'POST'])
def character_route(id):
	info = requests.get('https://rickandmortyapi.com/api/character/'+ id)
	dicc = info.json()
	name_character = dicc["name"]
	status_character = dicc["status"]
	tipo_character = dicc["type"]
	gender_character = dicc["gender"]
	origin = dicc["origin"]["name"]
	location_name = dicc["location"]["name"]
	print(f"location url es {dicc['location']['url']}")
	location_num = id_url_character(dicc["location"]["url"])
	img = dicc["image"]
	lista_url_episodios = dicc["episode"] 
	lista_id_episodios = []
	for url in lista_url_episodios:
		num = id_url_character(url)
		lista_id_episodios.append(num)
	episodes_objects = requests.get('https://rickandmortyapi.com/api/episode/'+ str(lista_id_episodios)).json()
	lista_info_total = [name_character, status_character, tipo_character, 
	gender_character, origin, location_name, img, episodes_objects, location_num]
	return render_template('character.html', info_total=lista_info_total)
	#return str(lista_info_total)



@app.route('/location/<string:id>', methods=['GET', 'POST'])
def location_route(id):
	print(f"en location rout recibimos {id}")
	info = requests.get('https://rickandmortyapi.com/api/location/'+ id)
	dicc = info.json()
	if int(id) != -1000:
		name = dicc["name"]
		type_ = dicc["type"]
		dimension = dicc["dimension"]
		residents_url = dicc["residents"]
		residents_id = []
		for url in residents_url:
			residents_id.append(id_url_character(url))
		objects_residents = requests.get('https://rickandmortyapi.com/api/character/'+ str(residents_id)).json()
		lista_info_total = [name, type_, dimension, objects_residents]
		return render_template('location.html', info_total=lista_info_total)
	else: 
		return "Unknow Location"

def id_url_character(url):
	print(f"se recibio a {url}")
	lista_separada = url.split("/")
	print(f"la lista en la funcion es {lista_separada}")
	if url == "":
		return -1000
	numero = int(lista_separada[len(lista_separada)- 1])
	return numero


if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', port=80)