# Importamos librerias necesarias
import snscrape.modules.twitter as sntwitter
import pandas as pd
import os
from tqdm import tqdm

print("¿Qué cuenta quieres scrapear? Introdúcela sin la @")
cuenta = input()

print("¿Cuántos tweets quieres extraer?")
cantidad = input()
cantidad = int(cantidad) -1
cantidadfinal = cantidad + 1

print("Introduce un nombre para el archivo .xlsx:")
nombrearchivo = input()

# Creamos una lista a la que añadir datos
tweets_list1 = []

# Usamos TwitterSearchScraper para rascar info y añadirlo a la lista
for i,tweet in enumerate(sntwitter.TwitterSearchScraper('from:'+ str(cuenta)).get_items()): # Declaramos el user
    if i>cantidad: #number of tweets you want to scrape
     break
    tweets_list1.append([tweet.date, tweet.url, tweet.id, tweet.rawContent, tweet.user.username]) # Declaramos los atributos que queremos    

# Barra de carga 1
loop = tqdm(total = cantidadfinal, position=0, leave=False)
for k in range(cantidadfinal):
    loop.set_description("Descargando tweets...".format(k))
    loop.update(1)
loop.close

# Creamos un dataframe para los tweets de arriba
tweets_df1 = pd.DataFrame(tweets_list1, columns=['Datetime', 'Url', 'Tweet Id', 'Text', 'Username'])

# Cambiamos el formato de la fecha
tweets_df1['Datetime'] = tweets_df1['Datetime'].dt.tz_localize(None)

# Cambio el formato de Tweet ID a texto para que no se corten los últimos números por la n otación científica de excel
tweets_df1['Tweet Id'] = tweets_df1['Tweet Id'].apply(lambda x: str(x))

# Exportamos en excel
tweets_df1.to_excel(f"{nombrearchivo}.xlsx")

# ruta archivo
directorio = os.path.abspath(f"{nombrearchivo}.xlsx")

# Mensaje de finalización
print("\n¡Listo!",f"{nombrearchivo}.xlsx"," ha sido generado.")
print("Se han descargado un total de " + str(cantidadfinal) + " tweets de https://www.twitter.com/" + str(cuenta) + " en el archivo " + str(directorio))