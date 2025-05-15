#!/usr/bin/env python3

import dagster as dg

from datainlet.aws.utils import ept_to_dem

@dg.asset(
    group_name="raw_pdal"
)
def EPT_NOAA_PDAL_DEM():
    ept_to_dem(
        'https://noaa-nos-coastal-lidar-pds.s3.amazonaws.com/entwine/geoid18/9413/ept.json'
    )
