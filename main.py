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


@app.route('/search', methods=['POST'])
def search():
	## retorna una lista de listas, episodes, characters and locations
	# Episodes
	lista_total = []
	arg_consulta = request.form['text']
   
	dicc_episodes = requests.get('https://rickandmortyapi.com/api/episode/?name='+arg_consulta).json()
	if "info" in dicc_episodes:
		numero_paginas_episodes= dicc_episodes["info"]["pages"]
		lista_episodios = []
		for episode_dic in dicc_episodes["results"]:
			lista_episodios.append(episode_dic)
		for i in range(numero_paginas_episodes - 1):
			next_pagina = dicc_episodes["info"]["next"]
			info_nueva_episodes = requests.get(next_pagina)
			dicc_episodes = info_nueva_episodes.json()
			for episode_dic in dicc_episodes["results"]:
				lista_episodios.append(episode_dic)
		lista_total.append(lista_episodios)
		#lista_completa_episodes.append(dicc)
		#lista_total.append(lista_episodios)
		#lista_total.append(lista_episodios)
	else:
		lista_total.append([])




	## Locations
	dicc_locations = requests.get('https://rickandmortyapi.com/api/location/?name='+arg_consulta).json()
	if "info" in dicc_locations:
		numero_paginas_locations= dicc_locations["info"]["pages"]
		lista_locations = []
		for location_dic in dicc_locations["results"]:
			lista_locations.append(location_dic)
		for i in range(numero_paginas_locations - 1):
			next_pagina = dicc_locations["info"]["next"]
			info_nueva_locations = requests.get(next_pagina)
			dicc_locations = info_nueva_locations.json()
			for locations_dic in dicc_locations["results"]:
				lista_locations.append(locations_dic)
		lista_total.append(lista_locations)
	else:
		lista_total.append([])




	## Characters
	dicc_characters = requests.get('https://rickandmortyapi.com/api/character/?name='+arg_consulta).json()
	if "info" in dicc_characters:
		numero_paginas_characters= dicc_characters["info"] ["pages"]
		lista_characters = []
		for character_dic in dicc_characters["results"]:
			lista_characters.append(character_dic)
		for i in range(numero_paginas_characters - 1):
			next_pagina = dicc_characters["info"]["next"]
			info_nueva_characters = requests.get(next_pagina)
			dicc_characters = info_nueva_characters.json()
			for characters_dic in dicc_characters["results"]:
				lista_characters.append(characters_dic)
		lista_total.append(lista_characters)

	else:
		lista_total.append([])
		
	

		


 
	return render_template('results_searchs.html', lista_total=lista_total)






if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', port=80)