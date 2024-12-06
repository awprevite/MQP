import arcpy

# Define the output directory and file name
output_directory = r"C:\Users\awpre\MQP_APP"  # Change this to your desired output folder
output_name = "my_point.shp"  # You can change this to a feature class name if saving in a geodatabase

# Define spatial reference (WGS 84 in this case)
spatial_ref = arcpy.SpatialReference(4326)  # EPSG: 4326 (WGS 84)

# Create the point geometry
point = arcpy.Point(-122.4194, 37.7749)  # Example: San Francisco coordinates
point_geometry = arcpy.PointGeometry(point, spatial_ref)

# Create a feature class to store the point
arcpy.CreateFeatureclass_management(
    out_path=output_directory,
    out_name=output_name,
    geometry_type="POINT",
    spatial_reference=spatial_ref
)

# Add the point to the feature class
feature_class = f"{output_directory}\\{output_name}"
with arcpy.da.InsertCursor(feature_class, ["SHAPE@"]) as cursor:
    cursor.insertRow([point_geometry])

print(f"Point created and saved to {feature_class}")
