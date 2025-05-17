#!/usr/bin/env python3
import json
import pdal
import subprocess

def ept_to_dem(
        ept_url,
        zmin=-50,
        zmax=500):

    bounds = f"([-64.87043,-64.7778], [17.668438, 17.70027])"
    res = 10/111111

    ept_reader = {
        "type": "readers.ept",
        "filename": ept_url,
        "bounds": bounds,
        "spatialreference": "COMPD_CS[\"NAD83(2011) / UTM zone 19N + NAVD88 height\",PROJCS[\"NAD83(2011) / UTM zone 19N\",GEOGCS[\"NAD83(2011)\",DATUM[\"NAD83_National_Spatial_Reference_System_2011\",SPHEROID[\"GRS 1980\",6378137,298.257222101,AUTHORITY[\"EPSG\",\"7019\"]],AUTHORITY[\"EPSG\",\"1116\"]],PRIMEM[\"Greenwich\",0,AUTHORITY[\"EPSG\",\"8901\"]],UNIT[\"degree\",0.0174532925199433,AUTHORITY[\"EPSG\",\"9122\"]],AUTHORITY[\"EPSG\",\"6318\"]],PROJECTION[\"Transverse_Mercator\"],PARAMETER[\"latitude_of_origin\",0],PARAMETER[\"central_meridian\",-69],PARAMETER[\"scale_factor\",0.9996],PARAMETER[\"false_easting\",500000],PARAMETER[\"false_northing\",0],UNIT[\"metre\",1,AUTHORITY[\"EPSG\",\"9001\"]],AXIS[\"Easting\",EAST],AXIS[\"Northing\",NORTH],AUTHORITY[\"EPSG\",\"6348\"]],VERT_CS[\"NAVD88 height\",VERT_DATUM[\"North American Vertical Datum 1988\",2005,AUTHORITY[\"EPSG\",\"5103\"]],UNIT[\"metre\",1,AUTHORITY[\"EPSG\",\"9001\"]],AXIS[\"Gravity-related height\",UP],AUTHORITY[\"EPSG\",\"5703\"]]]"

    }

    #range_filter = {
     #   "type": "filters.range",
    #    "limits":"Classification[2:2],Classification[40:40],Classification[41:41]"
   # }

    # polygon_filter = {
    #     "type": "filters.crop",
    #     "polygon": 'POLYGON((-65.399902 17.72044056, -64.55500000 17.72044056, -64.33500000 17.05607700, -65.399902 17.72044056))'
    # }

    # set_pdal_crs = {
    #     "type": "filters.reprojection",
    #     "in_srs": "EPSG:6348+5703",
    #     "out_srs": "EPSG:4326"
    # }

#    tiledb_writer = {
          #"type":"writers.tiledb",
          #"array_name": "USVI_TileDB"
          #}
          #
          #
    filter_info = {
        "type": "filters.info"
    }
    gdal_writer = {
        "type": "writers.gdal",
        "filename": "USVI_Geo.tif",
        "gdalopts": "compress=deflate",
        "nodata": -9999,
        "output_type": "idw",
        "resolution": 5.0,
        "window_size": 6,
        "override_srs": "EPSG:6348"
    }

    pipeline = json.dumps({"pipeline":[ept_reader, filter_info, gdal_writer]}, indent=2 )

    p = pdal.Pipeline(pipeline)
    p.execute()
