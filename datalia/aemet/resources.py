import datetime
import json

import dagster as dg
import httpx
from pydantic import PrivateAttr
from tenacity import retry, stop_after_attempt, wait_fixed

log = dg.get_dagster_logger()


class AEMETAPI(dg.ConfigurableResource):
    endpoint: str = "https://opendata.aemet.es/opendata/api"
    token: str

    _client: httpx.Client = PrivateAttr()

    def setup_for_execution(self, context: dg.InitResourceContext) -> None:
        transport = httpx.HTTPTransport(retries=5)
        limits = httpx.Limits(max_keepalive_connections=10, max_connections=10)

        self._client = httpx.Client(
            transport=transport, limits=limits, base_url=self.endpoint
        )

    @retry(stop=stop_after_attempt(5), wait=wait_fixed(30))
    def query_endpoint(self, url) -> dict:
        query = {
            "api_key": self.token,
        }

        response = self._client.get(url, params=query)
        response.raise_for_status()

        return response.json()

    @retry(stop=stop_after_attempt(5), wait=wait_fixed(30))
    def query_datos(self, response_data) -> dict:
        data_url = response_data.get("datos")

        if data_url is None:
            raise ValueError(f"The 'datos' field is not correct. {response_data}")

        r = self._client.get(data_url)

        r.raise_for_status()

        data = json.loads(r.text.encode("utf-8"))

        return data

    def get_weather_data(
        self, start_date: datetime.date, end_date: datetime.date, batch_size: int = 30
    ):
        start_date_str = start_date.strftime("%Y-%m-01") + "T00:00:00UTC"
        end_date_str = end_date.strftime("%Y-%m-01") + "T00:00:00UTC"

        current_date = start_date

        while current_date < end_date:
            next_date = min(
                current_date + datetime.timedelta(days=batch_size), end_date
            )

            start_date_str = current_date.strftime("%Y-%m-%d") + "T00:00:00UTC"
            end_date_str = next_date.strftime("%Y-%m-%d") + "T00:00:00UTC"

            url = f"/valores/climatologicos/diarios/datos/fechaini/{start_date_str}/fechafin/{end_date_str}/todasestaciones"
            endpoint_response_data = self.query_endpoint(url)
            data = self.query_datos(endpoint_response_data)

            current_date = next_date + datetime.timedelta(days=1)

            for item in data:
                yield item

    def get_all_stations(self):
        url = "/valores/climatologicos/inventarioestaciones/todasestaciones"

        endpoint_response_data = self.query_endpoint(url)
        data = self.query_datos(endpoint_response_data)

        return data

    def teardown_after_execution(self, context: dg.InitResourceContext) -> None:
        self._client.close()
