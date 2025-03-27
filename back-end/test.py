import arcpy

NETWORK_DATASET = r"C:\Users\awpre\OneDrive\Documents\ArcGIS\Projects\MyProject1\mqpgdb\CorrectedSidewalk.gdb\sidewalkfeaturedataset\sidewalknetworkdataset"
POLYGON_BARRIERS = r"C:\Users\awpre\OneDrive\Documents\ArcGIS\Packages\MQP All Costs and Data Layers_9847f1\commondata\finaldataset.gdb\Polygon_SixAmCost"
GDB_PATH = r"C:\Users\awpre\OneDrive\Documents\ArcGIS\Projects\MyProject1\mqpgdb\CorrectedSidewalk.gdb"

# Define the workspace and feature class
arcpy.env.workspace = GDB_PATH

print("Creating route layer...")
route_layer = arcpy.na.MakeRouteLayer(NETWORK_DATASET, "Route", "Length").getOutput(0)
print("Route layer created.")

print("Adding barriers to route layer...")
arcpy.na.AddLocations(route_layer, "Barrier", POLYGON_BARRIERS)

# Solve the route
arcpy.na.Solve(route_layer)
