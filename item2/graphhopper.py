import requests
from tabulate import tabulate

API_KEY = "e4009da4-72d9-4690-9acf-2e816a20d9bb"

transportes = {
    "1": "car",
    "2": "bike",
    "3": "foot"
}

def geocodificar(ciudad):
    url = "https://graphhopper.com/api/1/geocode"
    params = {
        "q": ciudad,
        "locale": "es",
        "key": API_KEY
    }

    respuesta = requests.get(url, params=params)
    datos = respuesta.json()

    if "hits" not in datos or len(datos["hits"]) == 0:
        return None

    punto = datos["hits"][0]["point"]
    return punto["lat"], punto["lng"]

while True:
    origen = input("Ciudad de Origen o 's' para salir: ")

    if origen.lower() == "s":
        print("Programa finalizado.")
        break

    destino = input("Ciudad de Destino o 's' para salir: ")

    if destino.lower() == "s":
        print("Programa finalizado.")
        break

    print("\nSeleccione medio de transporte:")
    print("1. Auto")
    print("2. Bicicleta")
    print("3. Caminando")

    opcion = input("Opción: ")
    vehiculo = transportes.get(opcion, "car")

    punto_origen = geocodificar(origen)
    punto_destino = geocodificar(destino)

    if punto_origen is None or punto_destino is None:
        print("No se pudo encontrar una de las ciudades.")
        continue

    url = "https://graphhopper.com/api/1/route"

    params = {
        "point": [
            f"{punto_origen[0]},{punto_origen[1]}",
            f"{punto_destino[0]},{punto_destino[1]}"
        ],
        "vehicle": vehiculo,
        "locale": "es",
        "instructions": "true",
        "calc_points": "true",
        "key": API_KEY
    }

    respuesta = requests.get(url, params=params)
    datos = respuesta.json()

    if "paths" not in datos:
        print("Error al calcular la ruta.")
        print(datos)
        continue

    ruta = datos["paths"][0]

    kilometros = ruta["distance"] / 1000
    millas = kilometros * 0.621371
    minutos = ruta["time"] / 60000

    horas = int(minutos // 60)
    minutos_restantes = int(minutos % 60)

    tabla = [
        ["Origen", origen],
        ["Destino", destino],
        ["Kilómetros", round(kilometros, 2)],
        ["Millas", round(millas, 2)],
        ["Duración", f"{horas} horas y {minutos_restantes} minutos"],
        ["Transporte", vehiculo]
    ]

    print("\nResultado del viaje:")
    print(tabulate(tabla, tablefmt="grid"))

    print("\nNarrativa del viaje:")
    for paso in ruta["instructions"]:
        print("-", paso["text"])

    print("\n")
