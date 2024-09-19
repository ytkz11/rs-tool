from PyQt5.QtCore import pyqtSlot, QUrl
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QApplication, QLineEdit
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel
import os, sys
import json
import folium
from folium.plugins import Draw, MousePosition


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('地图显示')
        self.resize(1000, 640)

        # Initialize the layout and web engine view
        self.init_ui()

        # Generate the map with drawing capabilities
        self.generate_map()

    def init_ui(self):
        """Initialize the UI layout."""
        layout = QVBoxLayout()
        self.qwebengine = QWebEngineView(self)
        layout.addWidget(self.qwebengine)

        # Add a line edit for displaying the drawn rectangle coordinates
        self.coordinates_display = QLineEdit(self)
        self.coordinates_display.setReadOnly(True)
        layout.addWidget(self.coordinates_display)

        container = QWidget(self)
        container.setLayout(layout)
        self.setCentralWidget(container)

    def generate_map(self):
        """Generate the map using Folium and add drawing tools."""
        location = [30.2899, 120.1568]
        folium_map = folium.Map(
            location=location,
            zoom_start=10,
            control_scale=True,
            tiles='http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}',
            attr='default'
        )

        # Add drawing control (rectangle only)
        draw_control = Draw(
            export=True,
            filename="data.geojson",
            position="topleft",
            draw_options={
                'polyline': False,
                'rectangle': {'shapeOptions': {'color': '#f06'}},  # Enable rectangle drawing
                'circle': False,
                'marker': False,
                'polygon': False,
                'circlemarker': False
            },
            edit_options={
                'edit': True,
                'remove': True
            }
        )
        folium_map.add_child(draw_control)
        folium_map.add_child(MousePosition(position='bottomright'))

        # Save map to HTML
        map_file_path = "index.html"
        folium_map.save(map_file_path)

        # Append the custom JavaScript to handle drawing events
        self.append_javascript(map_file_path)

        # Load the HTML map into QWebEngineView
        self.qwebengine.load(QUrl.fromLocalFile(os.path.abspath(map_file_path)))

        # Set up the web channel for communication between JavaScript and Python
        self.setup_web_channel()

    def append_javascript(self, file_path):
        """Append JavaScript for handling the draw event."""
        js_script = """
            <script>
                document.addEventListener('DOMContentLoaded', function() {
                    console.log("Map loaded.");
                    var mapInstance = L.map('map');  // Correctly initialize the map

                    mapInstance.on('click', function (event) {
                        var layer = event.layer;
                        var geojsonData = layer.toGeoJSON();  // Get GeoJSON of drawn layer
                        console.log("Draw event captured: ", geojsonData);

                        // Send GeoJSON data to Python
                        window.pywebviewApi.updateCoordinates(JSON.stringify(geojsonData));
                    });
                });
            </script>
        """
        with open(file_path, "a") as file:
            file.write(js_script)

    def setup_web_channel(self):
        """Set up the communication channel between JavaScript and Python."""
        self.web_channel = QWebChannel()
        self.web_channel.registerObject("pywebviewApi", self)
        self.qwebengine.page().setWebChannel(self.web_channel)

    @pyqtSlot(str)
    def updateCoordinates(self, message):
        """Update the coordinates display with the new GeoJSON data."""
        geojson = json.loads(message)
        print("Received GeoJSON:", geojson)

        geojson_dict = self.geojson_to_dict(geojson)

        # Process the geometry if it's a polygon (like the rectangle)
        if geojson_dict['geometry']['type'] == 'Polygon':
            coordinates = geojson_dict['geometry']['coordinates'][0]  # First set of coordinates for the rectangle
            print("Coordinates of the drawn rectangle:")

            # Print each coordinate
            for coord in coordinates:
                print(coord)

            # Format coordinates for display (lat, lon pairs)
            coords_str = ', '.join([f'({lon}, {lat})' for lon, lat in coordinates])  # lon, lat format
            self.coordinates_display.setText(coords_str)

        # Print the entire dictionary for reference
        print("Converted to Python dict:", geojson_dict)

    def geojson_to_dict(self, geojson):
        """Convert GeoJSON into a Python dictionary."""
        return {
            'type': geojson.get('type', 'Feature'),
            'geometry': geojson.get('geometry', {}),
            'properties': geojson.get('properties', {})
        }


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
