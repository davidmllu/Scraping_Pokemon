import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine

url = "https://www.wikidex.net"
lista_pokemon = "/wiki/Lista_de_Pokemon"

url_lista = url+lista_pokemon

respuesta = requests.get(url_lista)


df = pd.DataFrame(columns=['num_pokedex', 'nombre', 'tipo1', 'tipo2', 'habilidad1', 'habilidad2', 'hab_oculta', 
                           'peso', 'altura', 'ps', 'ataque', 'defensa', 'spatk', 'spdef', 'velocidad'])

if respuesta.status_code == 200:
    soup = BeautifulSoup(respuesta.text, "html.parser")

    for fila in soup.find_all("tr"):  
            cell = fila.find_all("td")
            if len(cell)==4:
                second_td = cell[1]
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
