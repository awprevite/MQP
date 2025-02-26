from flask import Flask, request, jsonify
from flask_cors import CORS
import arcpy
import os
import json
import geopandas as gpd
import pyproj

GDB_PATH = r"C:\Users\awpre\OneDrive\Documents\ArcGIS\Projects\MyProject1\mqpgdb\CorrectedSidewalk.gdb"
NETWORK_DATASET = r"C:\Users\awpre\OneDrive\Documents\ArcGIS\Projects\MyProject1\mqpgdb\CorrectedSidewalk.gdb\sidewalkfeaturedataset\sidewalknetworkdataset"
STOPS_FEATURE_CLASS = os.path.join(GDB_PATH, "Stops")
ROUTE_OUTPUT = os.path.join(GDB_PATH, "RouteOutput")
SHAPEFILE_OUTPUT = r"C:\Users\awpre\MQP_APP\outputs\RouteOutput.shp"
GEOJSON_OUTPUT = r"C:\Users\awpre\MQP_APP\front-end\public\RouteOutput.geojson"
GEOJSON_CONVERTED = r"C:\Users\awpre\MQP_APP\front-end\public\RouteOutputConverted.geojson"
# Fix these paths when running on windows laptop

app = Flask(__name__)
CORS(app)
@app.route('/temp', methods=['POST'])
def solve_route():

    try:
        data = request.get_json()
        print(f"Received data: {data}")

        if not data or 'start' not in data or 'end' not in data:
            print("Invalid input detected.")
            return jsonify({"error": "Invalid input. Provide 'start' and 'end' coordinates."}), 400
        
        start = data['start']
        startLat = start['lat']
        startLng = start['lng']
        end = data['end']
        endLat = end['lat']
        endLng = end['lng']
        print(f"Start coordinates: ({startLat}, {startLng}), End coordinates: ({endLat}, {endLng})")

        try:
            # Network Analyst extension
            arcpy.CheckOutExtension("Network")
            print("Checked out Network Analyst extension.")

            # Create or overwrite Stops feature class
            if arcpy.Exists(STOPS_FEATURE_CLASS):
                print("Deleting existing Stops feature class...")
                arcpy.management.Delete(STOPS_FEATURE_CLASS)
            print("Creating Stops feature class...")
            arcpy.management.CreateFeatureclass(GDB_PATH, "Stops", "POINT", spatial_reference=arcpy.SpatialReference(4326))
            arcpy.management.AddField(STOPS_FEATURE_CLASS, "Name", "TEXT")

            # Insert start and end points
            print("Inserting start and end points into Stops...")
            with arcpy.da.InsertCursor(STOPS_FEATURE_CLASS, ["SHAPE@XY", "Name"]) as cursor:
                cursor.insertRow([(startLng, startLat), "Start"])
                cursor.insertRow([(endLng, endLat), "End"])

            # Create route layer
            print("Creating route layer...")
            route_layer = arcpy.na.MakeRouteLayer(NETWORK_DATASET, "Route", "Length").getOutput(0)
            print("Route layer created.")

            # Add stops to route layer
            print("Adding stops to route layer...")
            arcpy.na.AddLocations(route_layer, "Stops", STOPS_FEATURE_CLASS, "", 1000)

            # Solve route
            print("Solving route...")
            arcpy.na.Solve(route_layer)
            print("Route solved.")

            # Save route results
            if arcpy.Exists(ROUTE_OUTPUT):
                print("Deleting existing RouteOutput...")
                arcpy.management.Delete(ROUTE_OUTPUT)
            print("Saving route results to geodatabase...")
            arcpy.management.CopyFeatures(f"{route_layer}/Routes", ROUTE_OUTPUT)

            # Save as shapefile
            if arcpy.Exists(SHAPEFILE_OUTPUT):
                print("Deleting existing shapefile...")
                arcpy.management.Delete(SHAPEFILE_OUTPUT)
            print("Saving route results to shapefile...")
            arcpy.management.CopyFeatures(f"{route_layer}/Routes", SHAPEFILE_OUTPUT)

            print(f"Route saved to: {ROUTE_OUTPUT} (Geodatabase)")
            print(f"Route saved to: {SHAPEFILE_OUTPUT} (Shapefile)")

            # Save and convert to GeoJSON
            if arcpy.Exists(GEOJSON_OUTPUT):
                print("Deleting existing geojson...")
                arcpy.management.Delete(GEOJSON_OUTPUT)
            print("Converting to geojson...")
            gdf = gpd.read_file(SHAPEFILE_OUTPUT)
            gdf.to_file(GEOJSON_OUTPUT, driver='GeoJSON')
            #arcpy.FeaturesToJSON_conversion(SHAPEFILE_OUTPUT, GEOJSON_OUTPUT, "FORMATTED")

            # Convert projection
            print("Converting projection...")
            source_crs = pyproj.CRS("EPSG:2249")  # Your source CRS
            target_crs = pyproj.CRS("EPSG:4326")  # WGS84 (lat, lon)

            # Create the transformation object
            transformer = pyproj.Transformer.from_crs(source_crs, target_crs, always_xy=True)

            # Load your GeoJSON file
            with open(GEOJSON_OUTPUT, "r") as f:
                geojson_data = json.load(f)

            # Function to convert coordinates of each feature
            def convert_coordinates(geojson_data):
                for feature in geojson_data["features"]:
                    # Check if the geometry is of type "LineString"
                    if feature["geometry"]["type"] == "LineString":
                        # Reproject each coordinate pair in the LineString
                        feature["geometry"]["coordinates"] = [
                            list(transformer.transform(x, y)) for x, y in feature["geometry"]["coordinates"]
                        ]

            # Convert the coordinates
            convert_coordinates(geojson_data)

            # Save the converted GeoJSON to a new file
            with open(GEOJSON_CONVERTED, "w") as f:
                json.dump(geojson_data, f)

            # Return the converted GeoJson
            with open(GEOJSON_CONVERTED, "r") as f:
                return jsonify(json.load(f))

        except Exception as e:
            print(f"Arcpy error: {e}")
            return jsonify({"error": f"Arcpy error: {str(e)}"}), 500

        finally:
            # Release Network Analyst extension
            arcpy.CheckInExtension("Network")
            print("Checked in Network Analyst extension.")

    except Exception as e:
        print(f"Flask error: {e}")
        return jsonify({"error": str(e)}), 500

        
# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
