#!/usr/bin/env python3
import json
import pdal
import subprocess

def ept_to_dem(
        ept_url,
        zmin=-50,
        zmax=500):

    bounds = f"([-65.399902,-64.55500000], [17.05607700,17.7204405],[{zmin},{zmax}])/EPSG:4326"
    res = 10/111111

    ept_reader = {
        "type": "readers.ept",
        "filename": ept_url,
        "bounds": bounds,
        "spatialreference": "EPSG:6348+5703"
    }

    range_filter = {
        "type": "filters.range",
        "limits":"Classification[2:2],Classification[40:40],Classification[41:41],Classification[43:43],Classification[45:45]"
    }

    polygon_filter = {
        "type": "filters.crop",
        "polygon": 'POLYGON((-65.399902 17.72044056, -64.55500000 17.72044056, -64.33500000 17.05607700))'
    }

    set_pdal_crs = {
        "type": "filters.reprojection",
        "in_srs": "EPSG:6348+5703",
        "out_srs": "EPSG:4326"
    }

    dem_writer = {
        "type": "writers.gdal",
        "gdaldriver": "GTiff",
        "filename": '/data/raw/USVI.tif',
        "binmode": True,
        "dimension": "Z",
        "data_type": "float64",
        "output_type": "mean",
        "resolution": res,
        "nodata": -99999,
        "gdalopts": "COMPRESS=LZW,TILED=YES,NUM_THREADS=ALL_CPUS"
    }
    pipeline = json.dumps({"pipeline":[ept_reader, range_filter, polygon_filter, set_pdal_crs, dem_writer]}, indent=2 )

    p = pdal.Pipeline(pipeline)
    p.execute()

    subprocess.run(["gdaladdo", "-r", "bilinear", '/data/raw/USVI.tif'])
