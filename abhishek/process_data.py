from abhishek.config_schemas.data_processing_config_schema import DataProcessingConfig
from abhishek.utils.config_utils import get_config
from abhishek.utils.gcp_utils import access_secret_version
from abhishek.utils.data_utils import get_raw_data_with_version
from hydra.utils import instantiate


@get_config(config_path="../configs", config_name="data_processing_config")
def process_data(config: DataProcessingConfig) -> None: 
    # print(config)
    # print(60*"#")
    # from omegaconf import OmegaConf
    # print(OmegaConf.to_yaml(config))
    # return 
   
    get_raw_data_with_version(
    version=config.version,
    data_local_save_dir=config.data_local_save_dir,
    dvc_remote_repo=config.dvc_remote_repo,
    dvc_data_folder=config.dvc_data_folder,
    github_user_name=config.github_user_name,
    github_access_token="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"
    )
    
    dataset_reader_manager = instantiate(config.dataset_reader_manager)
    dataset_cleaner_manager = instantiate(config.dataset_cleaner_manager)
    
    df = dataset_reader_manager.read_data().compute()
    sample_df = df.sample(n=5)

    for _, row in sample_df.iterrows():
        text = row["text"]
        cleaned_text = dataset_cleaner_manager(text)
        
        print(60 * "#")
        print(f"text={text}")
        print(f"cleaned_text={cleaned_text}")
        print(60 * "#")



if __name__ == "__main__":
    process_data()  # type: ignore
    