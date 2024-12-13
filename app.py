from flask import Flask, render_template, request, jsonify
import folium

app = Flask(__name__)

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

# Página principal
@app.route("/")
def index():
    # Crear el mapa en la ubicación actual
    m = folium.Map(location=[gps_data["latitude"], gps_data["longitude"]], zoom_start=15)
    folium.Marker(
        location=[gps_data["latitude"], gps_data["longitude"]],
        popup=f"Lat: {gps_data['latitude']}, Lon: {gps_data['longitude']}",
        tooltip="Última ubicación",
    ).add_to(m)

    # Renderizar el mapa en HTML
    map_html = m._repr_html_()
    return render_template("index.html", map_html=map_html, gps_data=gps_data)

# Ruta para recibir datos del ESP32
@app.route("/update", methods=["POST"])
def update_data():
    data = request.get_json()
    global gps_data
    gps_data.update(data)
    return jsonify({"status": "success", "message": "Datos actualizados"})

if __name__ == "__main__":
    app.run(debug=True)
