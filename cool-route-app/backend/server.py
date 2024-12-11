from flask import Flask, request, jsonify
from flask_cors import CORS
import arcpy

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Paths to your data (replace placeholders with actual paths)
GDB_PATH = "<path_to_your_geodatabase>"
NETWORK_DATASET = "<path_to_your_network_dataset>"
STOPS_FEATURE_CLASS = f"{GDB_PATH}/Stops"
ROUTE_OUTPUT = f"{GDB_PATH}/RouteOutput"

# Route to handle coordinate input and solve route
@app.route('/solve-route', methods=['POST'])
def solve_route():
    try:
        # Parse JSON data from the request
        data = request.get_json()
        if not data or 'coordinates' not in data:
            return jsonify({"error": "Invalid input. Please provide coordinates."}), 400

        coordinates = data['coordinates']
        if len(coordinates) < 2:
            return jsonify({"error": "At least two coordinates are required."}), 400

        # Ensure the Network Analyst extension is available
        arcpy.CheckOutExtension("Network")

        # Create a feature class for the stops
        arcpy.management.CreateFeatureclass(GDB_PATH, "Stops", "POINT", spatial_reference=arcpy.SpatialReference(4326))

        # Add fields for network stops (e.g., Name)
        arcpy.management.AddField(STOPS_FEATURE_CLASS, "Name", "TEXT")

        # Insert coordinates into the Stops feature class
        with arcpy.da.InsertCursor(STOPS_FEATURE_CLASS, ["SHAPE@XY", "Name"]) as cursor:
            for i, coord in enumerate(coordinates):
                cursor.insertRow([(coord[0], coord[1]), f"Stop {i + 1}"])

        # Create a route layer
        route_layer = arcpy.na.MakeRouteLayer(NETWORK_DATASET, "Route", "Length").getOutput(0)

        # Add Stops to the route layer
        arcpy.na.AddLocations(route_layer, "Stops", STOPS_FEATURE_CLASS)

        # Solve the route
        arcpy.na.Solve(route_layer)

        # Save the route result to a feature class
        arcpy.management.CopyFeatures(f"{route_layer}/Routes", ROUTE_OUTPUT)

        # Return success response
        return jsonify({"status": "Route solved successfully", "output": ROUTE_OUTPUT})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        # Release the Network Analyst extension
        arcpy.CheckInExtension("Network")

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
