import arcpy
import os
import json

# Paths to your data (update these to match your setup)

GDB_PATH = r"C:\Users\awpre\OneDrive\Documents\ArcGIS\Projects\MyProject1\MyProject1.gdb"
NETWORK_DATASET = r"C:\Users\awpre\OneDrive\Documents\ArcGIS\Projects\MyProject1\MyProject1.gdb\manual\nd1"
STOPS_FEATURE_CLASS = os.path.join(GDB_PATH, "Stops")
ROUTE_OUTPUT = os.path.join(GDB_PATH, "RouteOutput")  # Feature class for output
SHAPEFILE_OUTPUT = r"C:\Users\awpre\MQP_APP\outputs\RouteOutput.shp"  # Shapefile for easy viewing

# Route to handle coordinate input and solve route
def main():
    try:

        startLat = 42.2732403  # Latitude
        startLng = -71.8135398  # Longitude
        endLat = 42.2750496    # Latitude
        endLng = -71.8052906   # Longitude

        # Ensure the Network Analyst extension is available
        arcpy.CheckOutExtension("Network")

        # Create or overwrite the Stops feature class
        if arcpy.Exists(STOPS_FEATURE_CLASS):
            arcpy.management.Delete(STOPS_FEATURE_CLASS)
        arcpy.management.CreateFeatureclass(GDB_PATH, "Stops", "POINT", spatial_reference=arcpy.SpatialReference(4326))
        arcpy.management.AddField(STOPS_FEATURE_CLASS, "Name", "TEXT")

        # Insert start and end coordinates
        with arcpy.da.InsertCursor(STOPS_FEATURE_CLASS, ["SHAPE@XY", "Name"]) as cursor:
            cursor.insertRow([(startLng, startLat), "Start"])
            cursor.insertRow([(endLng, endLat), "End"])

        # Create a route layer
        route_layer = arcpy.na.MakeRouteLayer(NETWORK_DATASET, "Route", "Length").getOutput(0)

        # Add Stops to the route layer
        arcpy.na.AddLocations(route_layer, "Stops", STOPS_FEATURE_CLASS, "", 1000)

        # Solve the route
        arcpy.na.Solve(route_layer)

        # Save the route result to a feature class in the geodatabase
        if arcpy.Exists(ROUTE_OUTPUT):
            arcpy.management.Delete(ROUTE_OUTPUT)  # Delete existing output if it exists
        arcpy.management.CopyFeatures(f"{route_layer}/Routes", ROUTE_OUTPUT)

        # Save as a shapefile for easier viewing
        if arcpy.Exists(SHAPEFILE_OUTPUT):
            arcpy.management.Delete(SHAPEFILE_OUTPUT)  # Delete existing output if it exists
        arcpy.management.CopyFeatures(f"{route_layer}/Routes", SHAPEFILE_OUTPUT)

        print(f"Route saved to: {ROUTE_OUTPUT} (Geodatabase)")
        print(f"Route saved to: {SHAPEFILE_OUTPUT} (Shapefile)")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Release the Network Analyst extension
        arcpy.CheckInExtension("Network")

    '''
# Paths to your data (update these to match your setup)
GDB_PATH = r"C:\Users\awpre\MQP_APP\network\Geodatabase.gdb"
NETWORK_DATASET = r"C:\Users\awpre\MQP_APP\network\Geodatabase.gdb\sidewalkDataset\sidewalkNetworkDataset"
STOPS_FEATURE_CLASS = os.path.join(GDB_PATH, "Stops")
ROUTE_OUTPUT = os.path.join(GDB_PATH, "RouteOutput")

# Route to handle coordinate input and solve route
@app.route('/solve-route', methods=['POST'])
def solve_route():
    try:
        # Parse JSON data from the request
        data = request.get_json()
        if not data or 'start' not in data or 'end' not in data:
            return jsonify({"error": "Invalid input. Provide 'start' and 'end' coordinates."}), 400

        start = data['start']
        end = data['end']

        # Ensure the Network Analyst extension is available
        arcpy.CheckOutExtension("Network")

        # Create or overwrite the Stops feature class
        if arcpy.Exists(STOPS_FEATURE_CLASS):
            arcpy.management.Delete(STOPS_FEATURE_CLASS)
        arcpy.management.CreateFeatureclass(GDB_PATH, "Stops", "POINT", spatial_reference=arcpy.SpatialReference(4326))
        arcpy.management.AddField(STOPS_FEATURE_CLASS, "Name", "TEXT")

        # Insert start and end coordinates
        with arcpy.da.InsertCursor(STOPS_FEATURE_CLASS, ["SHAPE@XY", "Name"]) as cursor:
            cursor.insertRow([(start["lng"], start["lat"]), "Start"])
            cursor.insertRow([(end["lng"], end["lat"]), "End"])

        # Create a route layer
        route_layer = arcpy.na.MakeRouteLayer(NETWORK_DATASET, "Route", "Length").getOutput(0)

        # Add Stops to the route layer
        arcpy.na.AddLocations(route_layer, "Stops", STOPS_FEATURE_CLASS)

        # Solve the route
        arcpy.na.Solve(route_layer)

        # Save the route result to a feature class
        arcpy.management.CopyFeatures(f"{route_layer}/Routes", ROUTE_OUTPUT)

        # Extract route geometry for GeoJSON response
        route_geojson = []
        with arcpy.da.SearchCursor(ROUTE_OUTPUT, ["SHAPE@"]) as cursor:
            for row in cursor:
                geometry = row[0].JSON
                route_geojson.append(json.loads(geometry))

        # Return GeoJSON route
        return jsonify({"route": route_geojson}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        # Release the Network Analyst extension
        arcpy.CheckInExtension("Network")
'''

if __name__ == "__main__":
    main()
