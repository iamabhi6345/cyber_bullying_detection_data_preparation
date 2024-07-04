from abhishek.config_schemas.data_processing_config_schema import DataProcessingConfig
from abhishek.utils.config_utils import get_config
from abhishek.utils.gcp_utils import access_secret_version
from abhishek.utils.data_utils import get_raw_data_with_version


@get_config(config_path="../configs", config_name="data_processing_config")
def process_data(config: DataProcessingConfig) -> None: 
   
    get_raw_data_with_version(
    version=config.version,
    data_local_save_dir=config.data_local_save_dir,
    dvc_remote_repo=config.dvc_remote_repo,
    dvc_data_folder=config.dvc_data_folder,
    github_user_name=config.github_user_name,
    github_access_token="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"
    )


if __name__ == "__main__":
    process_data()  # type: ignore
    