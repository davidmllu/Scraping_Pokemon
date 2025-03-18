import requests
from bs4 import BeautifulSoup
import pandas as pd
import psycopg2



url = "https://www.wikidex.net/wiki/Kyurem"
respuesta = requests.get(url)


if respuesta.status_code == 200:
    soup = BeautifulSoup(respuesta.text, "html.parser")

    div_pokedex = soup.find("div", class_="sec sec-nacional")
    num_pokedex = div_pokedex.find("span", id="numeronacional").text.strip()


    nombre = soup.find("h1", class_="firstHeading").text.strip()


    try:
        fila_tipo = soup.find("tr", title="Tipos a los que pertenece")
        tipo_a = fila_tipo.find("td")
        tipo = tipo_a.find("a")
        tipo1 = tipo.attrs["href"]
        tipo2 = tipo.find_next_sibling().attrs["href"]
        
        url_tipo1 = "https://www.wikidex.net"+tipo1
        respuesta_tipo1 = requests.get(url_tipo1)
        if respuesta_tipo1.status_code == 200:
            soup = BeautifulSoup(respuesta_tipo1.text, "html.parser")

            tipo_final1 = soup.find("h1", class_="firstHeading").text.strip()

        else:
            print("error")

        url_tipo2 = "https://www.wikidex.net"+tipo2
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
        
        url_tipo1 = "https://www.wikidex.net"+tipo1
        respuesta_tipo1 = requests.get(url_tipo1)
        if respuesta_tipo1.status_code == 200:
            soup = BeautifulSoup(respuesta_tipo1.text, "html.parser")

            tipo_final1 = soup.find("h1", class_="firstHeading").text.strip()
        else:
            print("error")
    if respuesta.status_code == 200:
        soup = BeautifulSoup(respuesta.text, "html.parser")

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
            ps = td_ps.text.strip()

            td_atq = td_ps.find_next_sibling()
            atq = td_atq.text.strip()

            td_def = td_atq.find_next_sibling()
            defensa = td_def.text.strip()

            td_SpAtq = td_def.find_next_sibling()
            SpAtq = td_SpAtq.text.strip()

            td_SpDef = td_SpAtq.find_next_sibling()
            SpDef = td_SpDef.text.strip()

            td_vel = td_SpDef.find_next_sibling()
            Vel = td_vel.text.strip()
        

else:
     print("error")

df = pd.DataFrame(columns=['num_pokedex', 'nombre', 'tipo1', 'tipo2', 'habilidad1', 'habilidad2', 'hab_oculta', 
                           'peso', 'altura', 'ps', 'ataque', 'defensa', 'spatk', 'spdef', 'velocidad'])


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

from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:trabajo_pokemon@127.0.0.1:2642/pokedex')

df.to_sql(name='pokemon', con=engine, if_exists='append', index=False)
