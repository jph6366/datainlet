import datetime
import json

import httpx
from dagster import ConfigurableResource, InitResourceContext, get_dagster_logger
from pydantic import PrivateAttr
from tenacity import retry, stop_after_attempt, wait_exponential

log = get_dagster_logger()


class AEMETAPI(ConfigurableResource):
    endpoint: str = "https://opendata.aemet.es/opendata/api"
    token: str

    _client: httpx.Client = PrivateAttr()

    def setup_for_execution(self, context: InitResourceContext) -> None:
        transport = httpx.HTTPTransport(retries=5)
        limits = httpx.Limits(max_keepalive_connections=5, max_connections=10)
        self._client = httpx.Client(
            transport=transport,
            limits=limits,
            base_url=self.endpoint,
            timeout=20,
        )

    @retry(
        stop=stop_after_attempt(10),
        wait=wait_exponential(min=1, max=30),
    )
    def query(self, url):
        headers = {"cache-control": "no-cache"}

        query = {
            "api_key": self.token,
        }

        response = self._client.get(url, headers=headers, params=query)
        response.raise_for_status()

        if response.json().get("estado") == 404:
            log.info("No data found")
            return None

        data_url = response.json().get("datos")
        if data_url is None:
            raise ValueError(f"The 'datos' field is not correct. {response.json()}")

        r = self._client.get(data_url, timeout=30)
        r.raise_for_status()

        data = json.loads(r.text.encode("utf-8"))

        return data

    def get_weather_data(self, start_date: datetime.date, end_date: datetime.date):
        start_date_str = start_date.strftime("%Y-%m-01") + "T00:00:00UTC"
        end_date_str = end_date.strftime("%Y-%m-01") + "T00:00:00UTC"

        current_date = start_date

        while current_date < end_date:
            next_date = min(current_date + datetime.timedelta(days=14), end_date)

            start_date_str = current_date.strftime("%Y-%m-%d") + "T00:00:00UTC"
            end_date_str = next_date.strftime("%Y-%m-%d") + "T00:00:00UTC"

            log.info(f"Getting data from {start_date_str} to {end_date_str}")
            url = f"/valores/climatologicos/diarios/datos/fechaini/{start_date_str}/fechafin/{end_date_str}/todasestaciones"
            data = self.query(url)

            current_date = next_date + datetime.timedelta(days=1)

            yield data

    def get_all_stations(self):
        url = "/valores/climatologicos/inventarioestaciones/todasestaciones"

        return self.query(url)

    def teardown_after_execution(self, context: InitResourceContext) -> None:
        self._client.close()
