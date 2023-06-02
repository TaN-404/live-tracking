from flask import Flask, render_template
import geopy
import googlemaps
from datetime import datetime
import polyline
import folium
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Initialize Google Maps API client
gmaps = googlemaps.Client(key='AIzaSyD6JvemEJL-6CVcynPrTEEuOUG7fesOvGY')

# Geocoding function to convert address to coordinates
#geopy.geocoders.options.default_user_agent = "my-application"
geolocator = Nominatim(user_agent='http')

def geocode(address):
    location = geolocator.geocode(address)
    return location.latitude, location.longitude

# Function to get directions and decode the polyline
def get_directions(origin, destination):
    now = datetime.now()
    directions = gmaps.directions(origin, destination, departure_time=now)
    polyline_points = directions[0]['overview_polyline']['points']
    decoded_polyline = polyline.decode(polyline_points)
    return decoded_polyline

# Function to mark pickup points on the map
def mark_pickup_points(map, pickup_points):
    for pickup_point in pickup_points:
        folium.Marker(pickup_point, popup='Pickup Point').add_to(map)

# Function to show user's live location on the map
def show_live_location(origin, destination, pickup_points):
    # Get the directions and decode the polyline
    route = get_directions(origin, destination)

    # Create a map centered around the starting point
    map = folium.Map(location=origin, zoom_start=13)

    # Add a marker for the starting and ending points
    folium.Marker(origin, popup='Start').add_to(map)
    folium.Marker(destination, popup='Destination').add_to(map)

    # Add the decoded polyline to the map
    folium.PolyLine(route, color="blue", weight=2.5, opacity=1).add_to(map)

    # Mark pickup points on the map
    mark_pickup_points(map, pickup_points)

    # Return the map as an HTML string
    return map.get_root().render()

@app.route('/')
def index():
    # Define the origin, destination, and pickup points
    origin = geocode('Margao, Goa')
    destination = geocode('Panaji, Goa')
    pickup_points = [(15.453356, 73.865039), (15.427380, 73.893349)]  # List of pickup points

    # Show live location on the map
    map_html = show_live_location(origin, destination, pickup_points)

    return render_template('index.html', map_html=map_html)

if __name__ == '__main__':
    app.run()
