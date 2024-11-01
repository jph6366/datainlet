import httpx
from tenacity import retry, stop_after_attempt, wait_exponential
import dagster as dg


class MITECOArcGisAPI(dg.ConfigurableResource):
    endpoint: str = (
        "https://services-eu1.arcgis.com/RvnYk1PBUJ9rrAuT/ArcGIS/rest/services/"
    )

    @retry(
        stop=stop_after_attempt(10),
        wait=wait_exponential(multiplier=1, min=4, max=20),
    )
    def query(self, dataset_name, params=None):
        url = f"{self.endpoint}/{dataset_name}/FeatureServer/0/query"
        default_params = {"resultType": "standard", "outFields": "*", "f": "pjson"}
        query_params = {**default_params, **params} if params else default_params

        r = httpx.get(url, params=query_params)
        r.raise_for_status()

        return r.json()

    def get_water_reservoirs_data(self, start_date=None, end_date=None):
        if start_date and end_date:
            date_format = "%Y-%m-%d"
            params = {
                "where": f"fecha BETWEEN timestamp '{start_date.strftime(date_format)}' "
                f"AND timestamp '{end_date.strftime(date_format)}'"
            }
        else:
            params = None
        query_response = self.query(dataset_name="Embalses_Total", params=params)

        return query_response
