import csv
import yaml

def cargar_configuracion(ruta_config):
    with open(ruta_config, 'r') as config_file:
        configuracion = yaml.safe_load(config_file)
    return configuracion

def crear_lista_m3u(archivo_csv, nombre_lista_m3u, enlace_formato, condicion):
    with open(archivo_csv, 'r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=';')
        with open(nombre_lista_m3u, 'w', encoding='utf-8') as m3u_file:
            m3u_file.write('#EXTM3U\n')
            for row in reader:
                tipo = row['Tipo']
                id_acestream = row['ID']
                magnet = row['Magnet']
                calidad = f' [{row["Calidad"]}]' if row["Calidad"] else ''
                resolucion = f' [{row["Resolucion"]}]' if row["Resolucion"] else ''

                if condicion == 'torrserve':
                    if magnet:
                        enlace = enlace_formato.format(magnet=magnet)
                        if tipo == 'Serie':
                            m3u_file.write(f'#EXTINF:-1 group-title="{row["Titulo"]}" tvg-id="" tvg-logo="" ,{row["Titulo"]} (Cap {row["Capitulo"]}){calidad}{resolucion}\n{enlace}\n')
                        elif tipo == 'Pelicula':
                            m3u_file.write(f'#EXTINF:-1 group-title="{row["Año"]}" tvg-id="" tvg-logo="" ,{row["Titulo (Año)"]}{calidad}{resolucion}\n{enlace}\n')
                else:
                    if id_acestream != '0':
                        if condicion == 'horus' or condicion == 'get' or condicion == 'base':
                            enlace = enlace_formato.format(id_acestream=id_acestream, magnet=magnet)
                            if tipo == 'Serie':
                                m3u_file.write(f'#EXTINF:-1 group-title="{row["Titulo"]}" tvg-id="" tvg-logo="" ,{row["Titulo"]} (Cap {row["Capitulo"]}){calidad}{resolucion}\n{enlace}\n')
                            elif tipo == 'Pelicula':
                                m3u_file.write(f'#EXTINF:-1 group-title="{row["Año"]}" tvg-id="" tvg-logo="" ,{row["Titulo"]}{calidad}{resolucion}\n{enlace}\n')

# Cargar la configuración desde el archivo config.yaml
configuracion = cargar_configuracion('config.yaml')

# Crear listas M3U para torrserve (solo enlaces con magnet no vacío)
crear_lista_m3u(configuracion['ruta_csv'], configuracion['ruta_m3u_series_torrserve'], '{magnet}', 'torrserve')
crear_lista_m3u(configuracion['ruta_csv'], configuracion['ruta_m3u_peliculas_torrserve'], '{magnet}', 'torrserve')

# Crear listas M3U para horus, get y base (con ID distinto de 0)
crear_lista_m3u(configuracion['ruta_csv'], configuracion['ruta_m3u_series_horus'], 'plugin://script.module.horus?action=play&id={id_acestream}', 'horus')
crear_lista_m3u(configuracion['ruta_csv'], configuracion['ruta_m3u_peliculas_horus'], 'plugin://script.module.horus?action=play&id={id_acestream}', 'horus')
crear_lista_m3u(configuracion['ruta_csv'], configuracion['ruta_m3u_series_get'], 'http://127.0.0.1:6878/ace/getstream?id={id_acestream}', 'get')
crear_lista_m3u(configuracion['ruta_csv'], configuracion['ruta_m3u_peliculas_get'], 'http://127.0.0.1:6878/ace/getstream?id={id_acestream}', 'get')
crear_lista_m3u(configuracion['ruta_csv'], configuracion['ruta_m3u_series_base'], 'acestream://{id_acestream}', 'base')
crear_lista_m3u(configuracion['ruta_csv'], configuracion['ruta_m3u_peliculas_base'], 'acestream://{id_acestream}', 'base')
