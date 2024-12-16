import requests
import random
import time

# URL de tu aplicación en PythonAnywhere
url = "https://raymundoss.pythonanywhere.com/update"

# Punto central (Nueva York como ejemplo)
center_latitude = 40.7128
center_longitude = -74.0060

# Función para generar datos de prueba en zonas cercanas
def generate_position_data(center_lat, center_lon, radius=0.01):
    """
    Genera coordenadas aleatorias cercanas al punto central.
    - center_lat, center_lon: Coordenadas del centro
    - radius: Radio de la desviación en grados (aproximadamente 1 km)
    """
    new_lat = center_lat + random.uniform(-radius, radius)
    new_lon = center_lon + random.uniform(-radius, radius)
    return new_lat, new_lon

# Enviar múltiples solicitudes con datos generados
for _ in range(10):  # Cambia el rango para enviar más datos
    # Generar coordenadas cercanas
    latitude, longitude = generate_position_data(center_latitude, center_longitude)
    
    # Crear el JSON dinámicamente
    data = {
        "latitude": latitude,
        "longitude": longitude,
        "speed": random.randint(0, 100),  # Velocidad aleatoria entre 0 y 100
        "altitude": random.randint(0, 20),  # Altitud aleatoria entre 0 y 20
        "hdop": round(random.uniform(0.5, 2.0), 2),  # Precisión HDOP aleatoria
        "satellites": random.randint(4, 10),  # Número de satélites
        "time": "2024-12-15T12:00:00Z"  # Puedes actualizar esto dinámicamente si lo deseas
    }

    # Enviar la solicitud POST
    response = requests.post(url, json=data)

    # Mostrar la respuesta del servidor
    print("Enviado:", data)
    print("Código de estado:", response.status_code)
    print("Respuesta:", response.text)

    # Esperar un poco antes de enviar el siguiente (opcional)
    time.sleep(1)
