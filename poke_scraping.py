import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine

# URL inicial en la que hay la lista completa de pokemon
url = "https://www.wikidex.net"
lista_pokemon = "/wiki/Lista_de_Pokemon"

url_lista = url+lista_pokemon

respuesta = requests.get(url_lista)

# Creación del dataframe donde se almacenaran los datos extraidos.
df = pd.DataFrame(columns=['num_pokedex', 'nombre', 'tipo1', 'tipo2', 'habilidad1', 'habilidad2', 'hab_oculta', 
                           'peso', 'altura', 'ps', 'ataque', 'defensa', 'spatk', 'spdef', 'velocidad'])

if respuesta.status_code == 200:
    soup = BeautifulSoup(respuesta.text, "html.parser")

    # Mediante el for se buscan todos los tr de la página, que contienen el número, nombre, tipos y nombre en japonés.
    for fila in soup.find_all("tr"):  
            cell = fila.find_all("td")

            '''
            El objetivo a buscar es la URL asociada al nombre de cada pokemon para entrar a su página individual.
            Existe el problema de que hay pokemon que tienen formas regionales y el número es el mismo para los dos.
            En estos casos hay que buscar en lugar del segundo td(generalmente el nombre) a buscar el primero ya que el número corresponde a la forma normal.
            '''
            if len(cell)==4:
                second_td = cell[1]
                a_tag = second_td.find("a")
                pokemon = a_tag["href"]
              
                # Estas tres variables, es necesario resetearlas si no guardan el dato del pokemon anterior en caso de que el actual no tenga alguna de ellas.
                tipo_final2 = ""

                habilidad2 = ""

                habilidad_ocu = ""
              
                # Se conbinan la URL de la wikidex y la del pokemon para aceder a su página individual.
                url_pokemon = url+pokemon

                respuesta_pokemon = requests.get(url_pokemon)

                if respuesta_pokemon.status_code == 200:
                    soup = BeautifulSoup(respuesta_pokemon.text, "html.parser")
                  
                    # Se busca el div donde está el número de la pokedex nacional y se accede al número.
                    div_pokedex = soup.find("div", class_="sec sec-nacional")
                    num_pokedex = div_pokedex.find("span", id="numeronacional").text.strip()

                    # El nombre el el título de la página.
                    nombre = soup.find("h1", class_="firstHeading").text.strip()
                  

                    '''En el caso de los tipos hay que diferenciar si se tiene dos o uno.
                    Prueba a buscar los dos y si no encuentra el segundo pasa a ejecutar la busqueda de uno.
                    Los tipos en este caso se muestran con imagenes en la web así que se busca la URL asociada 
                    a las imagenes para aceder a la páginas del tipo buscado y coger el título de la página que incluye el tipo correspondiente
                    '''
                    try:
                        fila_tipo = soup.find("tr", title="Tipos a los que pertenece")
                        tipo_a = fila_tipo.find("td")
                        tipo = tipo_a.find("a")
                        tipo1 = tipo.attrs["href"]
                        tipo2 = tipo.find_next_sibling().attrs["href"]
                        
                        url_tipo1 = url+tipo1
                        respuesta_tipo1 = requests.get(url_tipo1)
                        if respuesta_tipo1.status_code == 200:
                            soup = BeautifulSoup(respuesta_tipo1.text, "html.parser")

                            tipo_final1 = soup.find("h1", class_="firstHeading").text.strip()

                        else:
                            print("error")

                        url_tipo2 = url+tipo2
                        respuesta_tipo2 = requests.get(url_tipo2)
                        if respuesta_tipo2.status_code == 200:
                            soup = BeautifulSoup(respuesta_tipo2.text, "html.parser")

                            tipo_final2 = soup.find("h1", class_="firstHeading").text.strip()
                        else:
                            print("error")
                    except:
                        fila_tipo = soup.find("tr", title="Tipos a los que pertenece")
                        tipo_a = fila_tipo.find("td")
                        tipo = tipo_a.find("a").attrs["href"]
                        
                        url_tipo1 = url+tipo1
                        respuesta_tipo1 = requests.get(url_tipo1)
                        if respuesta_tipo1.status_code == 200:
                            soup = BeautifulSoup(respuesta_tipo1.text, "html.parser")

                            tipo_final1 = soup.find("h1", class_="firstHeading").text.strip()
                        else:
                            print("error")

                    # Se vuelve de nuevo a la página del pokemon para segir.
                    if respuesta_pokemon.status_code == 200:
                        soup = BeautifulSoup(respuesta_pokemon.text, "html.parser")

                        '''
                        Las habilidades utilizan el mismo mecanismo de probar si hay dos o una.
                        Para encontrar las habilidaddes hay que buscar la fila donde se encuentran y buscar los siguientes elementos.
                        '''
                        try:
                            fila_habilidad = soup.find("tr", title="Habilidades que puede conocer")
                            comp = fila_habilidad.find("td")
                            comp1 = comp.find("br")
                            num_a = len(comp1)
                            fila = soup.find("a", title="Habilidad").next_element
                            fila1 = fila.find_next()
                            habilidad1 = fila1.find_next()
                            fila3 = habilidad1.find_next()
                            habilidad2 = fila3.find_next()
                            habilidad1 = habilidad1.text.strip()
                            habilidad2 = habilidad2.text.strip()

                        except:
                            fila_habilidad = soup.find("tr", title="Habilidades que puede conocer")
                            habilidad1 = fila_habilidad.find("td").text.strip()
                            pass

                        # No todos tienen habilidad oculta así que hay que comprobar si la tiene
                        try:
                            fila_habilidad_ocu = soup.find("tr", title="Habilidad oculta")
                            habilidad_ocu = fila_habilidad_ocu.find("td").text.strip()
                        except:
                            pass

                        # El peso y la altura al igual que la habilidad, se busca el tr donde estan y dentro el td que los almacena.
                        fila_peso = soup.find("tr", title="Peso del Pokémon")
                        peso = fila_peso.find("td").text.strip()


                        fila_altura = soup.find("tr", title="Altura del Pokémon")
                        altura = fila_altura.find("td").text.strip()

                      
                        '''
                        Para encontar las características existe una página con una tabla y el nombre y cada una de las características del pokemon.
                        Buscando la etiqueta "a" con el nombre de cada pokemon se pasa a buscar los siguientes elementos hasta pasar a la proxima etiqueta.
                        De esta manera pasando de etiqueta en etiqueta se consiguen las 6 características base.
                        Algunas de ellas cuentan con un superindice de explicación por lo que se usa descompose para purgarlas y que no las incluya en los datos.
                        '''
                        url_caracteristicas = "https://www.wikidex.net/wiki/Lista_de_Pok%C3%A9mon_con_sus_caracter%C3%ADsticas_base"
                        respuesta_caracteristicas = requests.get(url_caracteristicas)

                        if respuesta_caracteristicas.status_code == 200:
                            soup = BeautifulSoup(respuesta_caracteristicas.text, "html.parser")

                            td_ps = soup.find("a", title=nombre).next_element.next_element.next_element.next_element.next_sibling.next_element
                            for sup in td_ps.find_all('sup'):
                                sup.decompose()
                            ps = td_ps.text.strip()

                            td_atq = td_ps.find_next_sibling()
                            for sup in td_atq.find_all('sup'):
                                sup.decompose()
                            atq = td_atq.text.strip()

                            td_def = td_atq.find_next_sibling()
                            for sup in td_def.find_all('sup'):
                                sup.decompose()
                            defensa = td_def.text.strip()

                            td_SpAtq = td_def.find_next_sibling()
                            for sup in td_SpAtq.find_all('sup'):
                                sup.decompose()
                            SpAtq = td_SpAtq.text.strip()

                            td_SpDef = td_SpAtq.find_next_sibling()
                            for sup in td_SpDef.find_all('sup'):
                                sup.decompose()
                            SpDef = td_SpDef.text.strip()

                            td_vel = td_SpDef.find_next_sibling()
                            for sup in td_vel.find_all('sup'):
                                sup.decompose()
                            Vel = td_vel.text.strip()

                        try:
                            datos = pd.Series({'num_pokedex':num_pokedex, 'nombre':nombre, 
                                            'tipo1':tipo_final1, 'tipo2':tipo_final2, 
                                            'habilidad1':habilidad1, 'habilidad2':habilidad2, 'hab_oculta':habilidad_ocu, 
                                            'peso':peso, 'altura':altura, 
                                            'ps':ps, 'ataque':atq, 'defensa':defensa, 'spatk':SpAtq, 'spdef':SpDef, 'velocidad':Vel})

                        except NameError:
                            try:
                                datos = pd.Series({'num_pokedex':num_pokedex, 'nombre':nombre, 
                                                'tipo1':tipo_final1, 'tipo2':tipo_final2,
                                                'habilidad1':habilidad1, 'habilidad2':habilidad2, 
                                                'peso':peso, 'altura':altura, 
                                                'ps':ps, 'ataque':atq, 'defensa':defensa, 'spatk':SpAtq, 'spdef':SpDef, 'velocidad':Vel})
                            except NameError:
                                try:
                                    datos = pd.Series({'num_pokedex':num_pokedex, 'nombre':nombre, 
                                                    'tipo1':tipo_final1, 'tipo2':tipo_final2,
                                                    'habilidad1':habilidad1, 'hab_oculta':habilidad_ocu,
                                                    'peso':peso, 'altura':altura, 
                                                    'ps':ps, 'ataque':atq, 'defensa':defensa, 'spatk':SpAtq, 'spdef':SpDef, 'velocidad':Vel})
                                except NameError:
                                    try:
                                        datos = pd.Series({'num_pokedex':num_pokedex, 'nombre':nombre, 
                                                        'tipo1':tipo_final1, 'tipo2':tipo_final2,
                                                        'habilidad1':habilidad1,
                                                        'peso':peso, 'altura':altura, 
                                                        'ps':ps, 'ataque':atq, 'defensa':defensa, 'spatk':SpAtq, 'spdef':SpDef, 'velocidad':Vel})
                                    except NameError:
                                        try:
                                            datos = pd.Series({'num_pokedex':num_pokedex, 'nombre':nombre, 
                                                            'tipo1':tipo_final1,
                                                            'habilidad1':habilidad1,'habilidad2':habilidad2, 'hab_oculta':habilidad_ocu,
                                                            'peso':peso, 'altura':altura, 
                                                            'Ps':ps, 'ataque':atq, 'defensa':defensa, 'spatk':SpAtq, 'spdef':SpDef, 'velocidad':Vel})
                                        except NameError:
                                            try:
                                                datos = pd.Series({'num_pokedex':num_pokedex, 'nombre':nombre, 
                                                                'tipo1':tipo_final1,
                                                                'habilidad1':habilidad1,'habilidad2':habilidad2,
                                                                'peso':peso, 'altura':altura, 
                                                                'ps':ps, 'ataque':atq, 'defensa':defensa, 'spatk':SpAtq, 'spdef':SpDef, 'velocidad':Vel})
                                            except NameError:
                                                try:
                                                    datos = pd.Series({'num_pokedex':num_pokedex, 'nombre':nombre, 
                                                                    'tipo1':tipo_final1,
                                                                    'habilidad1':habilidad1,'hab_oculta':habilidad_ocu,
                                                                    'peso':peso, 'altura':altura, 
                                                                    'ps':ps, 'ataque':atq, 'defensa':defensa, 'spatk':SpAtq, 'spdef':SpDef, 'velocidad':Vel})
                                                except NameError:
                                                    datos = pd.Series({'num_pokedex':num_pokedex, 'nombre':nombre, 
                                                                    'tipo1':tipo_final1,
                                                                    'habilidad1':habilidad1,
                                                                    'peso':peso, 'altura':altura, 
                                                                    'ps':ps, 'ataque':atq, 'defensa':defensa, 'spatk':SpAtq, 'spdef':SpDef, 'velocidad':Vel})
                        
                        df = pd.concat([df, datos.to_frame().T], ignore_index=True)


            elif len(cell)==3:
                second_td = cell[0]
                a_tag = second_td.find("a")
                pokemon = a_tag["href"]

                tipo_final2 = ""

                habilidad2 = ""

                habilidad_ocu = ""

                url_pokemon = url+pokemon

                respuesta_pokemon = requests.get(url_pokemon)

                if respuesta_pokemon.status_code == 200:
                    soup = BeautifulSoup(respuesta_pokemon.text, "html.parser")

                    div_pokedex = soup.find("div", class_="sec sec-nacional")
                    num_pokedex = div_pokedex.find("span", id="numeronacional").text.strip()


                    nombre = soup.find("h1", class_="firstHeading").text.strip()


                    try:
                        fila_tipo = soup.find("tr", title="Tipos a los que pertenece")
                        tipo_a = fila_tipo.find("td")
                        tipo = tipo_a.find("a")
                        tipo1 = tipo.attrs["href"]
                        tipo2 = tipo.find_next_sibling().attrs["href"]
                        
                        url_tipo1 = url+tipo1
                        respuesta_tipo1 = requests.get(url_tipo1)
                        if respuesta_tipo1.status_code == 200:
                            soup = BeautifulSoup(respuesta_tipo1.text, "html.parser")

                            tipo_final1 = soup.find("h1", class_="firstHeading").text.strip()

                        else:
                            print("error")

                        url_tipo2 = url+tipo2
                        respuesta_tipo2 = requests.get(url_tipo2)
                        if respuesta_tipo2.status_code == 200:
                            soup = BeautifulSoup(respuesta_tipo2.text, "html.parser")

                            tipo_final2 = soup.find("h1", class_="firstHeading").text.strip()
                        else:
                            print("error")
                    except:
                        fila_tipo = soup.find("tr", title="Tipos a los que pertenece")
                        tipo_a = fila_tipo.find("td")
                        tipo = tipo_a.find("a").attrs["href"]
                        
                        url_tipo1 = url+tipo1
                        respuesta_tipo1 = requests.get(url_tipo1)
                        if respuesta_tipo1.status_code == 200:
                            soup = BeautifulSoup(respuesta_tipo1.text, "html.parser")

                            tipo_final1 = soup.find("h1", class_="firstHeading").text.strip()
                        else:
                            print("error")
                    if respuesta_pokemon.status_code == 200:
                        soup = BeautifulSoup(respuesta_pokemon.text, "html.parser")
                        
                        try:
                            fila_habilidad = soup.find("tr", title="Habilidades que puede conocer")
                            comp = fila_habilidad.find("td")
                            comp1 = comp.find("br")
                            num_a = len(comp1)
                            fila = soup.find("a", title="Habilidad").next_element
                            fila1 = fila.find_next()
                            habilidad1 = fila1.find_next()
                            fila3 = habilidad1.find_next()
                            habilidad2 = fila3.find_next()
                            habilidad1 = habilidad1.text.strip()
                            habilidad2 = habilidad2.text.strip()

                        except:
                            fila_habilidad = soup.find("tr", title="Habilidades que puede conocer")
                            habilidad1 = fila_habilidad.find("td").text.strip()
                            pass
                        
                        try:
                            fila_habilidad_ocu = soup.find("tr", title="Habilidad oculta")
                            habilidad_ocu = fila_habilidad_ocu.find("td").text.strip()
                        except:
                            pass

                        
                        fila_peso = soup.find("tr", title="Peso del Pokémon")
                        peso = fila_peso.find("td").text.strip()


                        fila_altura = soup.find("tr", title="Altura del Pokémon")
                        altura = fila_altura.find("td").text.strip()


                        url_caracteristicas = "https://www.wikidex.net/wiki/Lista_de_Pok%C3%A9mon_con_sus_caracter%C3%ADsticas_base"
                        respuesta_caracteristicas = requests.get(url_caracteristicas)

                        if respuesta_caracteristicas.status_code == 200:
                            soup = BeautifulSoup(respuesta_caracteristicas.text, "html.parser")

                            td_ps = soup.find("a", title=nombre).next_element.next_element.next_element.next_element.next_sibling.next_element
                            for sup in td_ps.find_all('sup'):
                                sup.decompose()
                            ps = td_ps.text.strip()

                            td_atq = td_ps.find_next_sibling()
                            for sup in td_atq.find_all('sup'):
                                sup.decompose()
                            atq = td_atq.text.strip()

                            td_def = td_atq.find_next_sibling()
                            for sup in td_def.find_all('sup'):
                                sup.decompose()
                            defensa = td_def.text.strip()

                            td_SpAtq = td_def.find_next_sibling()
                            for sup in td_SpAtq.find_all('sup'):
                                sup.decompose()
                            SpAtq = td_SpAtq.text.strip()

                            td_SpDef = td_SpAtq.find_next_sibling()
                            for sup in td_SpDef.find_all('sup'):
                                sup.decompose()
                            SpDef = td_SpDef.text.strip()

                            td_vel = td_SpDef.find_next_sibling()
                            for sup in td_vel.find_all('sup'):
                                sup.decompose()
                            Vel = td_vel.text.strip()

                        try:
                            datos = pd.Series({'num_pokedex':num_pokedex, 'nombre':nombre, 
                                            'tipo1':tipo_final1, 'tipo2':tipo_final2, 
                                            'habilidad1':habilidad1, 'habilidad2':habilidad2, 'hab_oculta':habilidad_ocu, 
                                            'peso':peso, 'altura':altura, 
                                            'ps':ps, 'ataque':atq, 'defensa':defensa, 'spatk':SpAtq, 'spdef':SpDef, 'velocidad':Vel})

                        except NameError:
                            try:
                                datos = pd.Series({'num_pokedex':num_pokedex, 'nombre':nombre, 
                                                'tipo1':tipo_final1, 'tipo2':tipo_final2,
                                                'habilidad1':habilidad1, 'habilidad2':habilidad2, 
                                                'peso':peso, 'altura':altura, 
                                                'ps':ps, 'ataque':atq, 'defensa':defensa, 'spatk':SpAtq, 'spdef':SpDef, 'velocidad':Vel})
                            except NameError:
                                try:
                                    datos = pd.Series({'num_pokedex':num_pokedex, 'nombre':nombre, 
                                                    'tipo1':tipo_final1, 'tipo2':tipo_final2,
                                                    'habilidad1':habilidad1, 'hab_oculta':habilidad_ocu,
                                                    'peso':peso, 'altura':altura, 
                                                    'ps':ps, 'ataque':atq, 'defensa':defensa, 'spatk':SpAtq, 'spdef':SpDef, 'velocidad':Vel})
                                except NameError:
                                    try:
                                        datos = pd.Series({'num_pokedex':num_pokedex, 'nombre':nombre, 
                                                        'tipo1':tipo_final1, 'tipo2':tipo_final2,
                                                        'habilidad1':habilidad1,
                                                        'peso':peso, 'altura':altura, 
                                                        'ps':ps, 'ataque':atq, 'defensa':defensa, 'spatk':SpAtq, 'spdef':SpDef, 'velocidad':Vel})
                                    except NameError:
                                        try:
                                            datos = pd.Series({'num_pokedex':num_pokedex, 'nombre':nombre, 
                                                            'tipo1':tipo_final1,
                                                            'habilidad1':habilidad1,'habilidad2':habilidad2, 'hab_oculta':habilidad_ocu,
                                                            'peso':peso, 'altura':altura, 
                                                            'Ps':ps, 'ataque':atq, 'defensa':defensa, 'spatk':SpAtq, 'spdef':SpDef, 'velocidad':Vel})
                                        except NameError:
                                            try:
                                                datos = pd.Series({'num_pokedex':num_pokedex, 'nombre':nombre, 
                                                                'tipo1':tipo_final1,
                                                                'habilidad1':habilidad1,'habilidad2':habilidad2,
                                                                'peso':peso, 'altura':altura, 
                                                                'ps':ps, 'ataque':atq, 'defensa':defensa, 'spatk':SpAtq, 'spdef':SpDef, 'velocidad':Vel})
                                            except NameError:
                                                try:
                                                    datos = pd.Series({'num_pokedex':num_pokedex, 'nombre':nombre, 
                                                                    'tipo1':tipo_final1,
                                                                    'habilidad1':habilidad1,'hab_oculta':habilidad_ocu,
                                                                    'peso':peso, 'altura':altura, 
                                                                    'ps':ps, 'ataque':atq, 'defensa':defensa, 'spatk':SpAtq, 'spdef':SpDef, 'velocidad':Vel})
                                                except NameError:
                                                    datos = pd.Series({'num_pokedex':num_pokedex, 'nombre':nombre, 
                                                                    'tipo1':tipo_final1,
                                                                    'habilidad1':habilidad1,
                                                                    'peso':peso, 'altura':altura, 
                                                                    'ps':ps, 'ataque':atq, 'defensa':defensa, 'spatk':SpAtq, 'spdef':SpDef, 'velocidad':Vel})
                                                
                        df = pd.concat([df, datos.to_frame().T], ignore_index=True)


    engine = create_engine('postgresql://postgres:contraseña@127.0.0.1:5432/pokedex')

    df.to_sql(name='pokemon', con=engine, if_exists='append', index=False)
