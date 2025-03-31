from flask import Flask, request, jsonify
from flask_cors import CORS
import arcpy
import os
import json
import geopandas as gpd
import pyproj

# Set up paths on server start up

# Stops features - RouteSolver\Stops
STOPS_FEATURE_NONE = r"C:\Users\awpre\OneDrive\Documents\ArcGIS\Projects\MyProject1\mqpgdb\CorrectedSidewalk.gdb\RouteSolver17k7mdg\Stops17acqog"
STOPS_FEATURE_6AM = r"C:\Users\awpre\OneDrive\Documents\ArcGIS\Projects\MyProject1\mqpgdb\CorrectedSidewalk.gdb\RouteSolver1wksl6g\Stops1wamxis"
STOPS_FEATURE_7AM = r"C:\Users\awpre\OneDrive\Documents\ArcGIS\Projects\MyProject1\mqpgdb\CorrectedSidewalk.gdb\RouteSolver1pc023s\Stops1p30evc"
STOPS_FEATURE_8AM = r"C:\Users\awpre\OneDrive\Documents\ArcGIS\Projects\MyProject1\mqpgdb\CorrectedSidewalk.gdb\RouteSolver17zj98w\Stops17qc79o"
STOPS_FEATURE_9AM = r"C:\Users\awpre\OneDrive\Documents\ArcGIS\Projects\MyProject1\mqpgdb\CorrectedSidewalk.gdb\RouteSolver1bzkxqs\Stops1btwebg"
STOPS_FEATURE_10AM = r"C:\Users\awpre\OneDrive\Documents\ArcGIS\Projects\MyProject1\mqpgdb\CorrectedSidewalk.gdb\RouteSolver1x9vihk\Stops1x0ldh4"
STOPS_FEATURE_11AM = r"C:\Users\awpre\OneDrive\Documents\ArcGIS\Projects\MyProject1\mqpgdb\CorrectedSidewalk.gdb\RouteSolver1st1u08\Stops1sjh3ig"
STOPS_FEATURE_12PM = r"C:\Users\awpre\OneDrive\Documents\ArcGIS\Projects\MyProject1\mqpgdb\CorrectedSidewalk.gdb\RouteSolver1vod4ng\Stops1vedsuk"
STOPS_FEATURE_1PM = r"C:\Users\awpre\OneDrive\Documents\ArcGIS\Projects\MyProject1\mqpgdb\CorrectedSidewalk.gdb\RouteSolver19wc7mc\Stops19mss70"
STOPS_FEATURE_2PM = r"C:\Users\awpre\OneDrive\Documents\ArcGIS\Projects\MyProject1\mqpgdb\CorrectedSidewalk.gdb\RouteSolver1wyubzc\Stops1wp5mw8"
STOPS_FEATURE_3PM = r"C:\Users\awpre\OneDrive\Documents\ArcGIS\Projects\MyProject1\mqpgdb\CorrectedSidewalk.gdb\RouteSolverx46pv8\Stopswui7vo"
STOPS_FEATURE_4PM = r"C:\Users\awpre\OneDrive\Documents\ArcGIS\Projects\MyProject1\mqpgdb\CorrectedSidewalk.gdb\RouteSolver1a8n75g\Stops1a35emk"
STOPS_FEATURE_5PM = r"C:\Users\awpre\OneDrive\Documents\ArcGIS\Projects\MyProject1\mqpgdb\CorrectedSidewalk.gdb\RouteSolver118xwck\Stops10yw8fw"
STOPS_FEATURE_6PM = r"C:\Users\awpre\OneDrive\Documents\ArcGIS\Projects\MyProject1\mqpgdb\CorrectedSidewalk.gdb\RouteSolver8jbc24\Stops88vr2k"
STOPS_FEATURE_7PM = r"C:\Users\awpre\OneDrive\Documents\ArcGIS\Projects\MyProject1\mqpgdb\CorrectedSidewalk.gdb\RouteSolver1371ncc\Stops12w9708"
STOPS_FEATURE_8PM = r"C:\Users\awpre\OneDrive\Documents\ArcGIS\Projects\MyProject1\mqpgdb\CorrectedSidewalk.gdb\RouteSolverfi4tfk\Stopsfb6xwo"

# route features - RouteSolver\Routes
ROUTE_FEATURE_NONE = r"C:\Users\awpre\OneDrive\Documents\ArcGIS\Projects\MyProject1\mqpgdb\CorrectedSidewalk.gdb\RouteSolver17k7mdg\Routes1qe65v8"
ROUTE_FEATURE_6AM = r"C:\Users\awpre\OneDrive\Documents\ArcGIS\Projects\MyProject1\mqpgdb\CorrectedSidewalk.gdb\RouteSolver1wksl6g\Routeshwwc78"
ROUTE_FEATURE_7AM = r"C:\Users\awpre\OneDrive\Documents\ArcGIS\Projects\MyProject1\mqpgdb\CorrectedSidewalk.gdb\RouteSolver1pc023s\Routes9r6uk8"
ROUTE_FEATURE_8AM = r"C:\Users\awpre\OneDrive\Documents\ArcGIS\Projects\MyProject1\mqpgdb\CorrectedSidewalk.gdb\RouteSolver17zj98w\Routes1quz26g"
ROUTE_FEATURE_9AM = r"C:\Users\awpre\OneDrive\Documents\ArcGIS\Projects\MyProject1\mqpgdb\CorrectedSidewalk.gdb\RouteSolver1bzkxqs\Routes1scdkiw"
ROUTE_FEATURE_10AM = r"C:\Users\awpre\OneDrive\Documents\ArcGIS\Projects\MyProject1\mqpgdb\CorrectedSidewalk.gdb\RouteSolver1x9vihk\Routeshfukqk"
ROUTE_FEATURE_11AM = r"C:\Users\awpre\OneDrive\Documents\ArcGIS\Projects\MyProject1\mqpgdb\CorrectedSidewalk.gdb\RouteSolver1st1u08\Routesd8jmao"
ROUTE_FEATURE_12PM = r"C:\Users\awpre\OneDrive\Documents\ArcGIS\Projects\MyProject1\mqpgdb\CorrectedSidewalk.gdb\RouteSolver1vod4ng\Routesf9k84k"
ROUTE_FEATURE_1PM = r"C:\Users\awpre\OneDrive\Documents\ArcGIS\Projects\MyProject1\mqpgdb\CorrectedSidewalk.gdb\RouteSolver19wc7mc\Routes1twhcv8"
ROUTE_FEATURE_2PM = r"C:\Users\awpre\OneDrive\Documents\ArcGIS\Projects\MyProject1\mqpgdb\CorrectedSidewalk.gdb\RouteSolver1wyubzc\Routesi7f8vk"
ROUTE_FEATURE_3PM = r"C:\Users\awpre\OneDrive\Documents\ArcGIS\Projects\MyProject1\mqpgdb\CorrectedSidewalk.gdb\RouteSolverx46pv8\Routes1jv18kc"
ROUTE_FEATURE_4PM = r"C:\Users\awpre\OneDrive\Documents\ArcGIS\Projects\MyProject1\mqpgdb\CorrectedSidewalk.gdb\RouteSolver1a8n75g\Routes1oqa8wo"
ROUTE_FEATURE_5PM = r"C:\Users\awpre\OneDrive\Documents\ArcGIS\Projects\MyProject1\mqpgdb\CorrectedSidewalk.gdb\RouteSolver118xwck\Routes1kbhwfg"
ROUTE_FEATURE_6PM = r"C:\Users\awpre\OneDrive\Documents\ArcGIS\Projects\MyProject1\mqpgdb\CorrectedSidewalk.gdb\RouteSolver8jbc24\Routesud6r9g"
ROUTE_FEATURE_7PM = r"C:\Users\awpre\OneDrive\Documents\ArcGIS\Projects\MyProject1\mqpgdb\CorrectedSidewalk.gdb\RouteSolver1371ncc\Routes1okt32k"
ROUTE_FEATURE_8PM = r"C:\Users\awpre\OneDrive\Documents\ArcGIS\Projects\MyProject1\mqpgdb\CorrectedSidewalk.gdb\RouteSolverfi4tfk\Routeswep2i0"

# Route layers - .lyrx route file
ROUTE_LAYER_NONE = r"C:\Users\awpre\OneDrive\Documents\ArcGIS\Projects\MyProject1\mqpgdb\none.lyrx"
ROUTE_LAYER_6AM = r"C:\Users\awpre\OneDrive\Documents\ArcGIS\Projects\MyProject1\mqpgdb\sixAM.lyrx"
ROUTE_LAYER_7AM = r"C:\Users\awpre\OneDrive\Documents\ArcGIS\Projects\MyProject1\mqpgdb\sevenAM.lyrx"
ROUTE_LAYER_8AM = r"C:\Users\awpre\OneDrive\Documents\ArcGIS\Projects\MyProject1\mqpgdb\eightAM.lyrx"
ROUTE_LAYER_9AM = r"C:\Users\awpre\OneDrive\Documents\ArcGIS\Projects\MyProject1\mqpgdb\nineAM.lyrx"
ROUTE_LAYER_10AM = r"C:\Users\awpre\OneDrive\Documents\ArcGIS\Projects\MyProject1\mqpgdb\tenAM.lyrx"
ROUTE_LAYER_11AM = r"C:\Users\awpre\OneDrive\Documents\ArcGIS\Projects\MyProject1\mqpgdb\elevenAM.lyrx"
ROUTE_LAYER_12PM = r"C:\Users\awpre\OneDrive\Documents\ArcGIS\Projects\MyProject1\mqpgdb\twelvePM.lyrx"
ROUTE_LAYER_1PM = r"C:\Users\awpre\OneDrive\Documents\ArcGIS\Projects\MyProject1\mqpgdb\onePM.lyrx"
ROUTE_LAYER_2PM = r"C:\Users\awpre\OneDrive\Documents\ArcGIS\Projects\MyProject1\mqpgdb\twoPM.lyrx"
ROUTE_LAYER_3PM = r"C:\Users\awpre\OneDrive\Documents\ArcGIS\Projects\MyProject1\mqpgdb\threePM.lyrx"
ROUTE_LAYER_4PM = r"C:\Users\awpre\OneDrive\Documents\ArcGIS\Projects\MyProject1\mqpgdb\fourPM.lyrx"
ROUTE_LAYER_5PM = r"C:\Users\awpre\OneDrive\Documents\ArcGIS\Projects\MyProject1\mqpgdb\fivePM.lyrx"
ROUTE_LAYER_6PM = r"C:\Users\awpre\OneDrive\Documents\ArcGIS\Projects\MyProject1\mqpgdb\sixPM.lyrx"
ROUTE_LAYER_7PM = r"C:\Users\awpre\OneDrive\Documents\ArcGIS\Projects\MyProject1\mqpgdb\sevenPM.lyrx"
ROUTE_LAYER_8PM = r"C:\Users\awpre\OneDrive\Documents\ArcGIS\Projects\MyProject1\mqpgdb\eightPM.lyrx"

GDB_PATH = r"C:\Users\awpre\OneDrive\Documents\ArcGIS\Projects\MyProject1\mqpgdb\CorrectedSidewalk.gdb"
NETWORK_DATASET = r"C:\Users\awpre\OneDrive\Documents\ArcGIS\Projects\MyProject1\mqpgdb\CorrectedSidewalk.gdb\sidewalkfeaturedataset\sidewalknetworkdataset"
STOPS_FEATURE_CLASS = os.path.join(GDB_PATH, "Stops")
ROUTE_OUTPUT = os.path.join(GDB_PATH, "RouteOutput")
STOPS_FEATURE_CLASS = os.path.join(GDB_PATH, "Stops")
ROUTE_OUTPUT = os.path.join(GDB_PATH, "RouteOutput")
SHAPEFILE_OUTPUT = r"C:\Users\awpre\MQP_APP\outputs\shapefileOutput.shp"
GEOJSON_OUTPUT = r"C:\Users\awpre\MQP_APP\outputs\geojsonOutput.shp"
GEOJSON_CONVERTED = r"C:\Users\awpre\MQP_APP\outputs\geojsonOutputConverted.shp"
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

            # Create route layer - replace with assiging route layer based on time
            #print("Creating route layer...")
            #route_layer = arcpy.na.MakeRouteLayer(NETWORK_DATASET, "Route", "Length").getOutput(0)
            #print("Route layer created.")

            # Assign stops feature
            print("Assigning stops feature...")
            STOPS_FEATURES = {
                '0': STOPS_FEATURE_NONE,
                '6': STOPS_FEATURE_6AM,
                '7': STOPS_FEATURE_7AM,
                '8': STOPS_FEATURE_8AM,
                '9': STOPS_FEATURE_9AM,
                '10': STOPS_FEATURE_10AM,
                '11': STOPS_FEATURE_11AM,
                '12': STOPS_FEATURE_12PM,
                '13': STOPS_FEATURE_1PM,
                '14': STOPS_FEATURE_2PM,
                '15': STOPS_FEATURE_3PM,
                '16': STOPS_FEATURE_4PM,
                '17': STOPS_FEATURE_5PM,
                '18': STOPS_FEATURE_6PM,
                '19': STOPS_FEATURE_7PM,
                '20': STOPS_FEATURE_8PM,
            }

            # Get the route layer based on the time
            stops_feature = STOPS_FEATURES.get(data['time'], STOPS_FEATURE_NONE)
            print(f"Using stops feature: {stops_feature}")

            # Removing stops
            print("Removing existing stops from stops feature...")
            arcpy.management.DeleteFeatures(stops_feature)

            # Assign route feature
            print("Assigning route feature...")
            ROUTE_FEATURES = {
                '0': ROUTE_FEATURE_NONE,
                '6': ROUTE_FEATURE_6AM,
                '7': ROUTE_FEATURE_7AM,
                '8': ROUTE_FEATURE_8AM,
                '9': ROUTE_FEATURE_9AM,
                '10': ROUTE_FEATURE_10AM,
                '11': ROUTE_FEATURE_11AM,
                '12': ROUTE_FEATURE_12PM,
                '13': ROUTE_FEATURE_1PM,
                '14': ROUTE_FEATURE_2PM,
                '15': ROUTE_FEATURE_3PM,
                '16': ROUTE_FEATURE_4PM,
                '17': ROUTE_FEATURE_5PM,
                '18': ROUTE_FEATURE_6PM,
                '19': ROUTE_FEATURE_7PM,
                '20': ROUTE_FEATURE_8PM,
            }

            # Get the route feature based on the time
            route_feature = ROUTE_FEATURES.get(data['time'], ROUTE_FEATURE_NONE)
            print(f"Using route feature: {route_feature}")

            # Assign route layer
            print("Assigning route feature...")
            ROUTE_LAYERS = {
                '0': ROUTE_LAYER_NONE,
                '6': ROUTE_LAYER_6AM,
                '7': ROUTE_LAYER_7AM,
                '8': ROUTE_LAYER_8AM,
                '9': ROUTE_LAYER_9AM,
                '10': ROUTE_LAYER_10AM,
                '11': ROUTE_LAYER_11AM,
                '12': ROUTE_LAYER_12PM,
                '13': ROUTE_LAYER_1PM,
                '14': ROUTE_LAYER_2PM,
                '15': ROUTE_LAYER_3PM,
                '16': ROUTE_LAYER_4PM,
                '17': ROUTE_LAYER_5PM,
                '18': ROUTE_LAYER_6PM,
                '19': ROUTE_LAYER_7PM,
                '20': ROUTE_LAYER_8PM,
            }

            # Get the route layer based on the time
            route_layer = ROUTE_LAYERS.get(data['time'], ROUTE_LAYER_NONE)
            print(f"Using route layer: {route_layer}")

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
            arcpy.management.CopyFeatures(route_feature, ROUTE_OUTPUT)

            # Save as shapefile
            if arcpy.Exists(SHAPEFILE_OUTPUT):
                print("Deleting existing shapefile...")
                arcpy.management.Delete(SHAPEFILE_OUTPUT)
            print("Saving route results to shapefile...")
            arcpy.management.CopyFeatures(route_feature, SHAPEFILE_OUTPUT)

            #print(f"Route saved to: {ROUTE_OUTPUT} (Geodatabase)")
            print(f"Route saved to: {SHAPEFILE_OUTPUT} (Shapefile)")

            # Save and convert to GeoJSON
            if arcpy.Exists(GEOJSON_OUTPUT):
                print("Deleting existing geojson...")
                arcpy.management.Delete(GEOJSON_OUTPUT)
            print("Converting to geojson...")
            gdf = gpd.read_file(SHAPEFILE_OUTPUT)
            gdf.to_file(GEOJSON_OUTPUT, driver='GeoJSON')
            #arcpy.FeaturesToJSON_conversion(SHAPEFILE_OUTPUT, GEOJSON_OUTPUT, "FORMATTED")

            # Convert projections
            print("Converting projection...")
            source_crs = pyproj.CRS("EPSG:2249")  # Your source CRS
            target_crs = pyproj.CRS("EPSG:4326")  # WGS84 (lat, lon)

            # Create the transformation object
            transformer = pyproj.Transformer.from_crs(source_crs, target_crs, always_xy=True)

            # Load your GeoJSON file
            with open(GEOJSON_OUTPUT, "r") as f:
                geojson_data = json.load(f)

            for feature in geojson_data["features"]:
                #Check if the geometry is of type "LineString"
                if feature["geometry"]["type"] == "LineString":
                #Reproject each coordinate pair in the LineString
                    feature["geometry"]["coordinates"] = [
                        list(transformer.transform(x, y)) for x, y in feature["geometry"]["coordinates"]
                    ]

            # Save the converted GeoJSON to a new file
            with open(GEOJSON_CONVERTED, "w") as f:
                json.dump(geojson_data, f, indent=4)

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
