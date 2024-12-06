# Filename - server.py

# Import flask and datetime module for showing date and time
from flask import Flask, jsonify
from flask_cors import CORS
import arcpy

# Initializing flask app
app = Flask(__name__)
CORS(app)

# Route for seeing a data
@app.route('/point', methods=['GET'])
def create_point():

    arcpy.env.overwriteOutput = True
    point = arcpy.Point(-71.4756, 42.1617) # Long, Lat
    point_geom = arcpy.PointGeometry(point)

    # Returning an api for showing in  reactjs
    return jsonify ({
        "type" : "Point",
        "coordinates" : [point_geom.centroid.X, point_geom.centroid.Y]
    })

def create_buffer():
    
    arcpy.env.overwriteOutput = True
    point = arcpy.Point(-71.8079, 42.2626)  # Long, Lat
    point_geom = arcpy.PointGeometry(point)

    # Buffer analysis
    buffer = point_geom.buffer(1000)  # Buffer of 1000 meters

    # Return the buffer as GeoJSON (simplified example)
    return jsonify({
        "type": "Polygon",
        "coordinates": [list([pt.X, pt.Y] for pt in buffer[0])]
    })
    
# Running app
if __name__ == '__main__':
    app.run(debug=True)