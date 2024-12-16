from flask import Flask, render_template, request, jsonify
import folium
import os

app = Flask(__name__)

# Variables globales
gps_data = {
    "latitude": 0.000000,  # Coordenadas predeterminadas
    "longitude": 0.000000,
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
    """Renderiza la página principal con el mapa."""
    return render_template("index.html", gps_data=gps_data)

# Ruta para obtener los datos actuales
@app.route("/current_position", methods=["GET"])
def current_position():
    """Devuelve los datos GPS actuales y la ruta en formato JSON."""
    return jsonify({
        "gps_data": gps_data,
        "route": route
    })

# Ruta para recibir datos del ESP32
@app.route("/update", methods=["POST"])
def update_data():
    """Actualiza los datos GPS recibidos en formato JSON."""
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
    """Limpia los datos de la ruta y elimina el archivo de texto."""
    global route
    route = []
    if os.path.exists(data_file):
        os.remove(data_file)
    return jsonify({"status": "success", "message": "Datos borrados"})

# Ruta para mostrar todos los datos
@app.route("/show_all", methods=["GET"])
def show_all_data():
    """Muestra todos los datos almacenados en el archivo."""
    if os.path.exists(data_file):
        with open(data_file, "r") as file:
            content = file.readlines()
    else:
        content = []
    return jsonify({"status": "success", "data": content})

if __name__ == "__main__":
    app.run(debug=True)
