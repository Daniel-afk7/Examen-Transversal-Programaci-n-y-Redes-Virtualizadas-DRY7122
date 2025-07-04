#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import sys

# Configuración GraphHopper
GRAPHOPPER_API_KEY = "c235d3ac-b6b7-4ea0-b98c-6cfc92a20433"
BASE_URL = "https://graphhopper.com/api/1/route"

# Medios de transporte
MEDIOS_TRANSPORTE = {
    '1': {'nombre': 'Auto', 'perfil': 'car'},
    '2': {'nombre': 'Bicicleta', 'perfil': 'bike'},
    '3': {'nombre': 'Caminando', 'perfil': 'foot'}
}

def obtener_coordenadas(lugar, pais):
    """Obtiene coordenadas usando GraphHopper"""
    params = {
        'q': f"{lugar}, {pais}",
        'key': GRAPHOPPER_API_KEY,
        'limit': 1
    }
    try:
        response = requests.get("https://graphhopper.com/api/1/geocode", params=params, timeout=10)
        data = response.json()
        if data.get('hits'):
            return (data['hits'][0]['point']['lat'], data['hits'][0]['point']['lng'])
        print(f"[ERROR] No se encontró: {lugar} en {pais}")
        return None
    except Exception as e:
        print(f"[ERROR] Conexión fallida: {str(e)}")
        return None

def calcular_ruta(origen, destino, medio):
    """Calcula ruta optimizada"""
    params = {
        'point': [f"{origen[0]},{origen[1]}", f"{destino[0]},{destino[1]}"],
        'vehicle': medio['perfil'],
        'key': GRAPHOPPER_API_KEY,
        'locale': 'es',
        'optimize': 'true',
        'instructions': 'true'
    }
    try:
        response = requests.get(BASE_URL, params=params, timeout=15)
        data = response.json()
        if data.get('paths'):
            distancia_km = data['paths'][0]['distance'] / 1000
            distancia_millas = distancia_km * 0.621371
            duracion_horas = data['paths'][0]['time'] / 3600000
            instrucciones = data['paths'][0]['instructions']
            return distancia_km, distancia_millas, duracion_horas, instrucciones
        print("[ERROR] Ruta no calculable")
        return None
    except Exception as e:
        print(f"[ERROR] API GraphHopper: {str(e)}")
        return None

def mostrar_narrativa(origen, destino, medio, km, millas, horas, instrucciones):
    """Muestra narrativa técnica sin decoraciones"""
    print("\n" + "="*80)
    print(f"NARRATIVA DE VIAJE: {origen} (Chile) -> {destino} (Argentina)")
    print(f"Medio: {medio['nombre']} | Distancia: {km:.1f} km ({millas:.1f} millas)")
    print(f"Duracion estimada: {horas:.1f} horas\n")
    
    print("DETALLE DE RUTA OPTIMIZADA:")
    for paso in instrucciones:
        print(f"- {paso['text']} ({paso['distance']/1000:.1f} km)")

def main():
    print("\n" + "="*80)
    print("CALCULADOR DE RUTAS CHILE-ARGENTINA (GraphHopper)")
    print("="*80)
    print("Instrucciones:")
    print("- Ingrese nombres de ciudades")
    print("- Escriba 's' para salir")
    print("="*80)

    while True:
        try:
            # Entrada de datos
            origen = input("\nCiudad de Origen (Chile): ").strip()
            if origen.lower() == 's': break

            destino = input("Ciudad de Destino (Argentina): ").strip()
            if destino.lower() == 's': break

            # Geocodificación
            coord_origen = obtener_coordenadas(origen, "Chile")
            coord_destino = obtener_coordenadas(destino, "Argentina")
            if not coord_origen or not coord_destino:
                continue

            # Selección de medio
            print("\nMedios disponibles:")
            for key, medio in MEDIOS_TRANSPORTE.items():
                print(f"{key}. {medio['nombre']}")

            opcion = input("\nOpcion (1-3): ").strip()
            medio = MEDIOS_TRANSPORTE.get(opcion, MEDIOS_TRANSPORTE['1'])

            # Cálculo de ruta
            resultado = calcular_ruta(coord_origen, coord_destino, medio)
            if resultado:
                distancia_km, distancia_millas, duracion_horas, instrucciones = resultado
                mostrar_narrativa(origen, destino, medio, distancia_km, distancia_millas, duracion_horas, instrucciones)

            if input("\nContinuar? (s=salir): ").lower() == 's':
                break

        except KeyboardInterrupt:
            print("\nEjecución cancelada")
            break

if __name__ == "__main__":
    # Verificación de dependencias
    try:
        import requests
    except ImportError:
        print("Instalando dependencias...")
        import subprocess
        subprocess.run([sys.executable, "-m", "pip", "install", "requests"], check=True)
    
    main()