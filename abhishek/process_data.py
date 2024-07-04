from abhishek.config_schemas.config_schema import Config
from abhishek.utils.config_utils import get_config
from abhishek.utils.gcp_utils import access_secret_version
from abhishek.utils.data_utils import get_raw_data_with_version


@get_config(config_path="../configs", config_name="config")
def process_data(config: Config) -> None: 
    version = "v1" 
    data_local_save_dir = "./data/raw" 
    dvc_remote_repo = "https://github.com/iamabhi6345/cyber_bullying_detection_dvc.git" 
    dvc_data_folder = "data/raw" 
    github_user_name = "iamabhi6345" 
    # github_access_token = access_secret_version("iamabhi6345", "abhishek-data-github-access-token") 
    github_access_token = "SECRET TOKENS DONOT COMMIT" 

    get_raw_data_with_version(
    version=version,
    data_local_save_dir=data_local_save_dir,
    dvc_remote_repo=dvc_remote_repo,
    dvc_data_folder=dvc_data_folder,
    github_user_name=github_user_name,
    github_access_token=github_access_token
    )


if __name__ == "__main__":
    process_data()  # type: ignore
    