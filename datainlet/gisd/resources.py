import dagster as dg
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

class GISDArcGISAPI(dg.ConfigurableResource):
    endpoint: str = (
        "https://services3.arcgis.com/9nfxWATFamVUTTGb/ArcGIS/rest/services/"
    )

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True
    )
    def query(self, dataset_name, params=None):
        url = f"{self.endpoint}/{dataset_name}/FeatureServer/0/query"
        default_params = {
            "where": "1=1",
            "outFields": "*",            # Comma-separated list of fields to include; "*" means all fields
            "returnGeometry": "true",    # Explicitly request feature geometries
            "f": "pjson"                 # Response format: pjson (pretty JSON) for easier reading
        }
        query_params = {**default_params, **(params or {})}

        r = httpx.get(url, params=query_params)
        r.raise_for_status()

        return r.json()
    

    def get_us_virgin_islands(self):
        query_response = self.query(dataset_name="US_Virgin_Islands")

        return query_response
