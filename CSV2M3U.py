import csv
import yaml
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def cargar_configuracion(ruta_config):
    with open(ruta_config, 'r') as config_file:
        configuracion = yaml.safe_load(config_file)
    return configuracion

def crear_lista_m3u(archivo_csv, nombre_lista_m3u, enlace_formato, condicion, tipo_filtro=None):
    with open(archivo_csv, 'r', encoding='latin-1') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=';')
        with open(nombre_lista_m3u, 'w', encoding='latin-1') as m3u_file:
            m3u_file.write('#EXTM3U\n')
            total_generados = 0
            for row in reader:
                tipo = row['Tipo']
                if tipo_filtro and tipo != tipo_filtro:
                    continue

                id_acestream = row['ID']
                magnet = row['Magnet']
                calidad = f' [{row["Calidad"]}]' if row["Calidad"] else ''
                resolucion = f' [{row["Resolucion"]}]' if row["Resolucion"] else ''

                if condicion == 'torrserve':
                    if magnet:
                        enlace = enlace_formato.format(magnet=magnet)
                        if tipo == 'Serie':
                            m3u_file.write(f'#EXTINF:-1 group-title="{row["Titulo"]}" tvg-id="" tvg-logo="{row["Url"]}" ,{row["Titulo"]} (Cap {row["Capitulo"]}){calidad}{resolucion}\n{enlace}\n')
                        elif tipo == 'Pelicula':
                            m3u_file.write(f'#EXTINF:-1 group-title="{row["Año"]}" tvg-id="" tvg-logo="{row["Url"]}" ,{row["Titulo (Año)"]}{calidad}{resolucion}\n{enlace}\n')
                        total_generados += 1
                else:
                    if id_acestream != '0':
                        if condicion == 'horus' or condicion == 'get' or condicion == 'base':
                            enlace = enlace_formato.format(id_acestream=id_acestream, magnet=magnet)
                            if tipo == 'Serie':
                                m3u_file.write(f'#EXTINF:-1 group-title="{row["Titulo"]}" tvg-id="" tvg-logo="{row["Url"]}" ,{row["Titulo"]} (Cap {row["Capitulo"]}){calidad}{resolucion}\n{enlace}\n')
                            elif tipo == 'Pelicula':
                                m3u_file.write(f'#EXTINF:-1 group-title="{row["Año"]}" tvg-id="" tvg-logo="{row["Url"]}" ,{row["Titulo"]}{calidad}{resolucion}\n{enlace}\n')
                            total_generados += 1

            if total_generados == 0:
                print(Fore.RED + f'No se generaron M3U para {nombre_lista_m3u}')
            else:
                print(Fore.GREEN + f'Se generaron {total_generados} M3U para {nombre_lista_m3u}')

# Cargar la configuración desde el archivo config.yaml
configuracion = cargar_configuracion('config.yaml')

# Crear listas M3U para torrserve (solo enlaces con magnet no vacío)
crear_lista_m3u(configuracion['ruta_csv'], configuracion['ruta_m3u_series_torrserve'], '{magnet}', 'torrserve', 'Serie')
crear_lista_m3u(configuracion['ruta_csv'], configuracion['ruta_m3u_peliculas_torrserve'], '{magnet}', 'torrserve', 'Pelicula')

# Crear listas M3U para horus, get y base (con ID distinto de 0)
crear_lista_m3u(configuracion['ruta_csv'], configuracion['ruta_m3u_series_horus'], 'plugin://script.module.horus?action=play&id={id_acestream}', 'horus', 'Serie')
crear_lista_m3u(configuracion['ruta_csv'], configuracion['ruta_m3u_peliculas_horus'], 'plugin://script.module.horus?action=play&id={id_acestream}', 'horus', 'Pelicula')
crear_lista_m3u(configuracion['ruta_csv'], configuracion['ruta_m3u_series_get'], 'http://127.0.0.1:6878/ace/getstream?id={id_acestream}', 'get', 'Serie')
crear_lista_m3u(configuracion['ruta_csv'], configuracion['ruta_m3u_peliculas_get'], 'http://127.0.0.1:6878/ace/getstream?id={id_acestream}', 'get', 'Pelicula')
crear_lista_m3u(configuracion['ruta_csv'], configuracion['ruta_m3u_series_base'], 'acestream://{id_acestream}', 'base', 'Serie')
crear_lista_m3u(configuracion['ruta_csv'], configuracion['ruta_m3u_peliculas_base'], 'acestream://{id_acestream}', 'base', 'Pelicula')
