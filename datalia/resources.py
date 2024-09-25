import datetime
import json
import os
import tempfile
from typing import Optional

import httpx
import polars as pl
import yaml
from dagster import ConfigurableResource, InitResourceContext, get_dagster_logger
from huggingface_hub import HfApi
from pydantic import PrivateAttr
from tenacity import retry, stop_after_attempt, wait_exponential

log = get_dagster_logger()


class DatasetPublisher(ConfigurableResource):
    hf_token: str

    _api: HfApi = PrivateAttr()

    def setup_for_execution(self, context: InitResourceContext) -> None:
        self._api = HfApi(token=self.hf_token)

    def publish(
        self,
        dataset: pl.DataFrame,
        dataset_name: str,
        username: str,
        readme: Optional[str] = None,
        generate_datapackage: bool = False,
    ):
        with tempfile.TemporaryDirectory() as temp_dir:
            # Define the file path
            data_dir = os.path.join(temp_dir, "data")
            os.makedirs(data_dir, exist_ok=True)
            file_path = os.path.join(data_dir, f"{dataset_name}.parquet")

            # Write the dataset to a parquet file
            dataset.write_parquet(file_path)

            if readme:
                readme_path = os.path.join(temp_dir, "README.md")
                with open(readme_path, "w") as readme_file:
                    readme_file.write(readme)

            if generate_datapackage:
                datapackage = {
                    "name": dataset_name,
                    "resources": [
                        {"path": f"data/{dataset_name}.parquet", "format": "parquet"}
                    ],
                }
                datapackage_path = os.path.join(temp_dir, "datapackage.yaml")
                with open(datapackage_path, "w") as dp_file:
                    yaml.dump(datapackage, dp_file)

            # Check if the repository exists
            repo_id = f"{username}/{dataset_name}"

            try:
                self._api.repo_info(repo_id=repo_id, repo_type="dataset")
                log.info(f"Repository {repo_id} exists.")
            except Exception:
                log.info(
                    f"Repository {repo_id} does not exist. Creating a new repository."
                )
                self._api.create_repo(
                    repo_id=repo_id, repo_type="dataset", private=False
                )

            # Upload the entire folder to Hugging Face
            self._api.upload_large_folder(
                folder_path=temp_dir, repo_id=repo_id, repo_type="dataset"
            )


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

        data_url = response.json().get("datos")
        if data_url is None:
            raise ValueError(f"The 'datos' field is not correct. {response.json()}")

        r = self._client.get(data_url, timeout=30)
        r.raise_for_status()

        data = json.loads(r.text.encode("utf-8"))

        return data

    def get_weather_data(
        self, start_date: datetime.datetime, end_date: datetime.datetime
    ):
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
