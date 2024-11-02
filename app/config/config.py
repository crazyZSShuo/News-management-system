from dynaconf import Dynaconf
import glob

from pathlib import Path


__all__ = ("config", )

ROOT_DIR = Path(__file__).parent


def read_files(file_path: str) -> list:
    return glob.glob(file_path, root_dir=ROOT_DIR)


confs = read_files("default/*.yml")

config = Dynaconf(
    settings_files=confs,
    core_loaders=["YAML"],
    load_dotenv=True,
    root_path=ROOT_DIR
)