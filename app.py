from flask import Flask, render_template, request, jsonify, redirect, url_for
import folium
import os
import json

app = Flask(__name__)

# Archivo donde se guardarán las posiciones
GPS_DATA_FILE = "gps_data.txt"

# Variable global para almacenar las coordenadas
gps_data = {
    "latitude": 0,
    "longitude": 0,
    "speed": 0,
    "altitude": 0,
    "hdop": 0,
    "satellites": 0,
    "time": ""
}

# Ruta principal
@app.route("/")
def index():
    # Leer posiciones almacenadas
    if os.path.exists(GPS_DATA_FILE):
        with open(GPS_DATA_FILE, "r") as file:
            positions = [json.loads(line.strip()) for line in file.readlines()]
    else:
        positions = []

    # Crear el mapa
    if positions:
        last_position = positions[-1]
        m = folium.Map(location=[last_position["latitude"], last_position["longitude"]], zoom_start=15)

        # Dibujar la ruta
        route = [[pos["latitude"], pos["longitude"]] for pos in positions]
        folium.PolyLine(route, color="blue", weight=2.5).add_to(m)

        # Añadir marcador en la última posición
        folium.Marker(
            location=[last_position["latitude"], last_position["longitude"]],
            popup=f"Lat: {last_position['latitude']}, Lon: {last_position['longitude']}",
            tooltip="Última ubicación",
        ).add_to(m)
    else:
        # Mapa predeterminado si no hay datos
        m = folium.Map(location=[gps_data["latitude"], gps_data["longitude"]], zoom_start=2)

    # Renderizar mapa en HTML
    map_html = m._repr_html_()
    return render_template("index.html", map_html=map_html, gps_data=gps_data)

# Ruta para recibir datos del ESP32
@app.route("/update", methods=["POST"])
def update_data():
    data = request.get_json()
    global gps_data
    gps_data.update(data)

    # Guardar datos en un archivo
    with open(GPS_DATA_FILE, "a") as file:
        file.write(json.dumps(data) + "\n")

    return jsonify({"status": "success", "message": "Datos actualizados"})

# Ruta para borrar los datos almacenados
@app.route("/clear", methods=["POST"])
def clear_data():
    if os.path.exists(GPS_DATA_FILE):
        os.remove(GPS_DATA_FILE)
    return redirect(url_for("index"))

# Ruta para mostrar todos los datos almacenados
@app.route("/show", methods=["GET"])
def show_data():
    if os.path.exists(GPS_DATA_FILE):
        with open(GPS_DATA_FILE, "r") as file:
            positions = [json.loads(line.strip()) for line in file.readlines()]
        return jsonify({"status": "success", "positions": positions})
    return jsonify({"status": "error", "message": "No hay datos almacenados"})

if __name__ == "__main__":
    app.run(debug=True)
