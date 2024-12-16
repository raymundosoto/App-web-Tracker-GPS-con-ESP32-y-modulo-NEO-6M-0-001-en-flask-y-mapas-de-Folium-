from flask import Flask, render_template, request, jsonify
import folium
import os

app = Flask(__name__)

# Variables globales
gps_data = {
    "latitude": 0.000000,  # Coordenadas predeterminadas (Nueva York)
    "longitude": -0.00000,
    "speed": 0.0,
    "altitude": 0.0,
    "hdop": 0.0,
    "satellites": 0,
    "time": ""
}
route = []  # Para almacenar las coordenadas
data_file = "gps_data.txt"  # Archivo para almacenar datos GPS

# Página principal
@app.route("/")
def index():
    # Crear el mapa con la última ubicación
    m = folium.Map(location=[gps_data["latitude"], gps_data["longitude"]], zoom_start=15)
    
    # Dibujar la ruta en el mapa si hay datos
    if route:
        folium.PolyLine(route, color="blue", weight=2.5, opacity=0.8).add_to(m)
    
    # Añadir un marcador en la última posición
    folium.Marker(
        location=[gps_data["latitude"], gps_data["longitude"]],
        popup=f"Lat: {gps_data['latitude']}, Lon: {gps_data['longitude']}",
        tooltip="Última ubicación",
        icon=folium.Icon(color="red")
    ).add_to(m)

    # Renderizar el mapa en HTML
    map_html = m._repr_html_()
    return render_template("index.html", map_html=map_html, gps_data=gps_data)

# Ruta para recibir datos del ESP32
@app.route("/update", methods=["POST"])
def update_data():
    data = request.get_json()
    global gps_data, route

    gps_data.update(data)
    route.append([gps_data["latitude"], gps_data["longitude"]])

    # Guardar los datos en el archivo de texto
    with open(data_file, "a") as file:
        file.write(f"{data}\n")

    return jsonify({"status": "success", "message": "Datos actualizados"})

# Ruta para borrar datos
@app.route("/clear", methods=["POST"])
def clear_data():
    global route
    route = []
    if os.path.exists(data_file):
        os.remove(data_file)
    return jsonify({"status": "success", "message": "Datos borrados"})

# Ruta para mostrar todos los datos
@app.route("/show_all", methods=["GET"])
def show_all_data():
    if os.path.exists(data_file):
        with open(data_file, "r") as file:
            content = file.readlines()
    else:
        content = []
    return jsonify({"status": "success", "data": content})

if __name__ == "__main__":
    app.run(debug=True)
