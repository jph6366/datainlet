#!/usr/bin/env python3

import dagster as dg

from datainlet.aws.utils import ept_to_dem

@dg.asset()
def EPT_PDAL_TILEDB() -> dg.MaterializeResult :
    ept_to_dem(
        'https://noaa-nos-coastal-lidar-pds.s3.amazonaws.com/entwine/geoid18/9413/ept.json'
    )

#tiledb_pybabylon_viz_notebook = define_dagstermill_asset(
   #     name="tiledb_viz_nb",
  #      notebook_path=dg.file_relative_path(__file__, "notebooks/tiledb.ipynb"),
 #       io_manager_key="output_notebook_io_manager"
#    )
