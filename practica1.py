#!/usr/bin/python3

import webapp

contents_key_value = {}
contents_value_key = {}

archivo = open('f_dict_key_value.txt','r')  

while True: 
	linea = archivo.readline()  # lee línea
	if not linea: 
		break 
	datos = linea.split(',');
	contents_key_value[datos[0]] = datos[1].split('\n')[0]
		 
archivo.close  

archivo = open('f_dict_value_key.txt','r')  

while True: 
	linea = archivo.readline()  # lee línea
	if not linea: 
		break 
	datos = linea.split(',');
	contents_value_key[datos[0]] = datos[1].split('\n')[0]
		 
archivo.close

formulario = """
 <form action="" method="POST">
  URL:<br>
  <input type="text" name="URL" value=""><br>
  <input type="submit" value="Acortar">
</form> 
"""

class acortadorApp(webapp.webApp):
	def parse(self, request):
		return (request.split()[0], request.split()[1], request)
		
	def process(self, parsedRequest): 
		metodo, recurso, peticion = parsedRequest
		if metodo == "GET":
			if recurso =="/":
				respuesta = ""
				for key, value in contents_key_value.items():
					respuesta += '<p><a href = ' + '"' + value + '">' + key + '</a>' + '--> ' + '<a href = ' + '"' + value + '">' + value + '</a>'             
                                        
				return("200 OK", "<html><body>" + formulario + respuesta + '</p></body></html></html>')
	
			else:			
				try:				 
					respuesta = '<head> <META HTTP-EQUIV="REFRESH" CONTENT="0;URL=' + contents_key_value[recurso] + '"> </head>'
					return("301 Moved Permanently", "<html>" + respuesta + '</html>')	
				except KeyError:
					respuesta = 'URL no encontrada' + '<br>'
					return("404 Not Found", "<html>" + formulario + respuesta + '</html>')					

		if metodo == "POST":
			peticion_procesada = peticion.split('\r\n\r\n',1)[1].split('=')[1] 
			if peticion_procesada == "":
				respuesta = 'Error: introduce url a acortar' + '<br>' 
				return("200 OK", "<html>" + formulario + respuesta + '</html>')	

			else:
				if (peticion_procesada.find('http%3A%2F%2F') == 0) or (peticion_procesada.find('https%3A%2F%2F') == 0):

					peticion_procesada = peticion_procesada.split('%3A%2F%2F')[0] + '://'  + peticion_procesada.split('%3A%2F%2F')[1] 
					if peticion_procesada in contents_value_key:
						respuesta = contents_value_key[peticion_procesada]
						return("200 OK", '<html><body>' + formulario + '<p><a href = ' + '"' + contents_key_value[respuesta] + '">' + respuesta + '</a>' + '--> ' + '<a href = ' + '"' + contents_key_value[respuesta] + '">' + contents_key_value[respuesta] + '</a>' +'</p></body></html></html>')	
	
					else:									
						contents_key_value['/' + str(len(contents_key_value))] = peticion_procesada
						contents_value_key[peticion_procesada] = '/' + str(len(contents_value_key))
						respuesta = contents_value_key[peticion_procesada]

						myfile1 = open("f_dict_key_value.txt", "w")						
						for key, value in contents_key_value.items(): #guardamos en fichero
							linea = key + ',' + value + '\r\n'
							myfile1.write(linea)							
						myfile1.close()
  						
						myfile2 = open("f_dict_value_key.txt", "w")						
						for key, value in contents_value_key.items(): #guardamos en fichero
							linea = key + ',' + value + '\r\n'
							myfile2.write(linea)							
						myfile2.close()

						return("200 OK", '<html><body>' + formulario + '<p><a href = ' + '"' + contents_key_value[respuesta] + '">' + respuesta + '</a>' + '--> ' + '<a href = ' + '"' + contents_key_value[respuesta] + '">' + contents_key_value[respuesta] + '</a>' +'</p></body></html></html>')	

				else:
					peticion_procesada = 'http://' + peticion_procesada
					if peticion_procesada in contents_value_key:
						respuesta = contents_value_key[peticion_procesada]
						return("200 OK", '<html><body>' + formulario + '<p><a href = ' + '"' + contents_key_value[respuesta] + '">' + respuesta + '</a>' + '--> ' + '<a href = ' + '"' + contents_key_value[respuesta] + '">' + contents_key_value[respuesta] + '</a>' +'</p></body></html></html>')

					else:	
						contents_key_value['/' + str(len(contents_key_value))] = peticion_procesada
						contents_value_key[peticion_procesada] = '/' + str(len(contents_value_key)) 
						respuesta = contents_value_key[peticion_procesada]
						
						myfile1 = open("f_dict_key_value.txt", "w")						
						for key, value in contents_key_value.items(): #guardamos en fichero
							linea = key + ',' + value + '\r\n'
							myfile1.write(linea)							
						myfile1.close()
  						
						myfile2 = open("f_dict_value_key.txt", "w")						
						for key, value in contents_value_key.items(): #guardamos en fichero
							linea = key + ',' + value + '\r\n'
							myfile2.write(linea)							
						myfile2.close()

						return("200 OK", '<html><body>' + formulario + '<p><a href = ' + '"' + contents_key_value[respuesta] + '">' + respuesta + '</a>' + '--> ' + '<a href = ' + '"' + contents_key_value[respuesta] + '">' + contents_key_value[respuesta] + '</a>' +'</p></body></html></html>')
			
if __name__ == "__main__":
	testWebApp = acortadorApp("localhost", 4567)

