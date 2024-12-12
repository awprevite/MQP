from flask import Flask, request, jsonify
from flask_cors import CORS
import arcpy
import os
import json

# Initialize Flask app
app = Flask(__name__)
CORS(app)

@app.route('/temp', methods=['POST'])
def solve_route():
    try:
        data = request.get_json()

        if not data or 'start' not in data or 'end' not in data:
            return jsonify({"error": "Invalid input. Provide 'start' and 'end' coordinates."}), 400
        
        start = data['start']
        end = data['end']
        return jsonify({"success": "Coordinates received."}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
