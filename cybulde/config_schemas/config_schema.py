from hydra.core.config_store import ConfigStore
from pydantic.dataclasses import dataclass


@dataclass
class Config:
    dvc_remote_name: str = "cybulde-data"
    dvc_remote_url: str = "gdrive://1BM3pbLCrJ-MQRL92mT_ZC9tHDZH403ox"
    dvc_raw_data_folder: str = "data/raw"


def setup_config() -> None:
    cs = ConfigStore.instance()
    cs.store(name="config_schema", node=Config)
