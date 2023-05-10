from flask import Flask, request, render_template
import folium

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        # Do something with the latitude and longitude values

        # Create a Folium map with a marker at the GPS coordinates
        map = folium.Map(location=[latitude, longitude], zoom_start=15)
        folium.Marker(location=[latitude, longitude], tooltip='GPS Coordinates').add_to(map)

        # Render the template with the Folium map
        return render_template('map.html', map=map._repr_html_())
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
