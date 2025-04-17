from flask import Flask, request, jsonify
from flask_cors import CORS
import arcpy
import os
import json
import geopandas as gpd
import pyproj
from multiprocessing import Queue, Process

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

DIRECT_ROUTE_OUTPUT = os.path.join(GDB_PATH, "DirectRouteOutput")
DIRECT_SHAPEFILE_OUTPUT = r"C:\Users\awpre\MQP_APP\outputs\directShapefileOutput.shp"
DIRECT_GEOJSON_OUTPUT = r"C:\Users\awpre\MQP_APP\outputs\directGeojsonOutput.shp"
DIRECT_GEOJSON_CONVERTED = r"C:\Users\awpre\MQP_APP\outputs\directGeojsonOutputConverted.shp"

ROUTE_OUTPUT = os.path.join(GDB_PATH, "RouteOutput")
SHAPEFILE_OUTPUT = r"C:\Users\awpre\MQP_APP\outputs\shapefileOutput.shp"
GEOJSON_OUTPUT = r"C:\Users\awpre\MQP_APP\outputs\geojsonOutput.shp"
GEOJSON_CONVERTED = r"C:\Users\awpre\MQP_APP\outputs\geojsonOutputConverted.shp"

app = Flask(__name__)
CORS(app)

task_queue = Queue()
result_queue = Queue()

# Function to parse requests and then make the routes
def worker(task_queue, result_queue):
    # Poll for requests
    while True:
        task = task_queue.get()
        if task is None:
            break

        try:
            start = task['start']
            startLat = start['lat']
            startLng = start['lng']
            end = task['end']
            endLat = end['lat']
            endLng = end['lng']
            time = task['time']

            print(f"Start coordinates: ({startLat}, {startLng}), End coordinates: ({endLat}, {endLng}), Time: ({time})")

            if not task or 'start' not in task or 'end' not in task or 'time' not in task:
                print("Invalid input detected.")
                return jsonify({"error": "Invalid input. Provide 'start' and 'end' coordinates and 'time'."}), 400

            try:
                # Network Analyst extension
                print("Checking out Network Analyst extension...")
                arcpy.CheckOutExtension("Network")

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
                stops_feature = STOPS_FEATURES.get(time, STOPS_FEATURE_NONE)
                print(f"Using stops feature: {stops_feature}")

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
                route_feature = ROUTE_FEATURES.get(time, ROUTE_FEATURE_NONE)
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
                route_layer = ROUTE_LAYERS.get(time, ROUTE_LAYER_NONE)
                print(f"Using route layer: {route_layer}")

                # Generate selected route
                route = generateRoute(stops_feature, route_feature, route_layer, ROUTE_OUTPUT, SHAPEFILE_OUTPUT, GEOJSON_OUTPUT, GEOJSON_CONVERTED)

                # Generate direct route
                if(time != '0'):
                    direct_route = generateRoute(STOPS_FEATURE_NONE, ROUTE_FEATURE_NONE, ROUTE_LAYER_NONE, DIRECT_ROUTE_OUTPUT, DIRECT_SHAPEFILE_OUTPUT, DIRECT_GEOJSON_OUTPUT, DIRECT_GEOJSON_CONVERTED)
                else: 
                    direct_route = route

                result_queue.put({
                    "route": route, 
                    "direct_route": direct_route
                })
                
            except Exception as e:
                print(f"Arcpy error: {e}")
                result_queue.put({"error": f"Arcpy error: {str(e)}"})

            finally:
                # Release Network Analyst extension
                arcpy.CheckInExtension("Network")
                print("Checked in Network Analyst extension.")

        except Exception as e:
            print(f"Flask error: {e}")
            result_queue.put({"error": str(e)})
    
@app.route('/route', methods=['POST'])
def solve_route():
    # Put requests in the queue
    task = request.get_json()
    task_queue.put(task)

    result = result_queue.get()

    if "error" in result:
        return jsonify(result), 500
    return jsonify(result)
    
# Function to make the routes
def generateRoute(stops_feature, route_feature, route_layer, output, shapefileOutput, geojsonOutput, geojsonConvertedOutput):

    # Removing stops
    print("Removing existing stops from stops feature...")
    arcpy.management.DeleteFeatures(stops_feature)

    # Add stops to route layer
    print("Adding stops to route layer...")
    arcpy.na.AddLocations(route_layer, "Stops", STOPS_FEATURE_CLASS, "", 1000)

    # Solve route
    print("Solving route...")
    arcpy.na.Solve(route_layer)
    print("Route solved.")

    # Save route results
    if arcpy.Exists(output):
        print("Deleting existing RouteOutput...")
        arcpy.management.Delete(output)
    print("Saving route results to geodatabase...")
    arcpy.management.CopyFeatures(route_feature, output)

    # Save as shapefile
    if arcpy.Exists(shapefileOutput):
        print("Deleting existing shapefile...")
        arcpy.management.Delete(shapefileOutput)
    print("Saving route results to shapefile...")
    arcpy.management.CopyFeatures(route_feature, shapefileOutput)

    #print(f"Route saved to: {ROUTE_OUTPUT} (Geodatabase)")
    print(f"Route saved to: {shapefileOutput} (Shapefile)")

    # Save and convert to GeoJSON
    if arcpy.Exists(geojsonOutput):
        print("Deleting existing geojson...")
        arcpy.management.Delete(geojsonOutput)
    print("Converting to geojson...")
    gdf = gpd.read_file(shapefileOutput)
    gdf.to_file(geojsonOutput, driver='GeoJSON')

    # Convert projections
    print("Converting projection...")
    source_crs = pyproj.CRS("EPSG:2249")  # Compatible with leaflet
    target_crs = pyproj.CRS("EPSG:4326")  # WGS84 (lat, lon)

    # Create the transformation object
    transformer = pyproj.Transformer.from_crs(source_crs, target_crs, always_xy=True)

    # Load your GeoJSON file
    with open(geojsonOutput, "r") as f:
        geojson_data = json.load(f)

    for feature in geojson_data["features"]:
        #Check if the geometry is of type "LineString"
        if feature["geometry"]["type"] == "LineString":
        #Reproject each coordinate pair in the LineString
            feature["geometry"]["coordinates"] = [
                list(transformer.transform(x, y)) for x, y in feature["geometry"]["coordinates"]
            ]

    # Save the converted GeoJSON to a new file
    with open(geojsonConvertedOutput, "w") as f:
        json.dump(geojson_data, f, indent=4)

    # Return the converted GeoJson
    with open(geojsonConvertedOutput, "r") as f:
        return json.load(f)

        
# Run the Flask app
if __name__ == '__main__':

    from multiprocessing import freeze_support
    freeze_support()

    Process(target=worker, args=(task_queue, result_queue), daemon=True).start()

    app.run(port=5000)