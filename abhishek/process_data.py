# from abhishek.config_schemas.data_processing_config_schema import DataProcessingConfig
# from abhishek.utils.config_utils import get_config
# from abhishek.utils.gcp_utils import access_secret_version
# from abhishek.utils.data_utils import get_raw_data_with_version
# from hydra.utils import instantiate
# from dask.distributed import Client 
# from pathlib import Path
# from abhishek.utils.utils import get_logger
# import dask.dataframe as dd
# from abhishek.config_schemas.data_processing.dataset_cleaners_schema import DatasetCleanerManagerConfig

# def process_raw_data(
#     df_partition: dd.core.DataFrame, dataset_cleaner_manager: DatasetCleanerManagerConfig
# ) -> dd.core.Series:
#     processed_partition: dd.core.Series = df_partition["text"].apply(dataset_cleaner_manager)
#     return processed_partition




# @get_config(config_path="../configs", config_name="data_processing_config")
# def process_data(config: DataProcessingConfig) -> None: 
#     logger = get_logger(Path(__file__).name)
#     logger.info("Processing raw data..")
    
#     # print(config)
#     # print(60*"#")
#     # from omegaconf import OmegaConf
#     # print(OmegaConf.to_yaml(config))
#     # return
    
    
#     processed_data_save_dir = config.processed_data_save_dir
#     cluster = instantiate(config .dask_cluster)
#     client = Client(cluster)
    
#     try:
   
#         get_raw_data_with_version(
#         version=config.version,
#         data_local_save_dir=config.data_local_save_dir,
#         dvc_remote_repo=config.dvc_remote_repo,
#         dvc_data_folder=config.dvc_data_folder,
#         github_user_name=config.github_user_name,
#         github_access_token="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"
#         )
        
#         dataset_reader_manager = instantiate(config.dataset_reader_manager)
#         dataset_cleaner_manager = instantiate(config.dataset_cleaner_manager)
        
#         df = dataset_reader_manager.read_data(config.dask_cluster.n_workers)
#         print(3*"\n")
#         print(60*"#")
#         print(df.npartitions)
#         # exit(0)
        
#         logger.info("Cleaning data...")
        
#         df = df.assign( 
#             cleaned_text=df.map_partitions(
#                 process_raw_data,
#                 dataset_cleaner_manager=dataset_cleaner_manager,
#                 meta=("text", "object")
#             )
#         )
#         df = df.compute()
        
#         train_parquet_path = os.path.join(processed_data_save_dir, "train.parquet")
#         dev_parquet_path = os.path.join(processed_data_save_dir, "dev.parquet")
#         test_parquet_path = os.path.join(processed_data_save_dir, "test.parquet")
        
#         df[df["split"] == "train"].to_parquet(train_parquet_path)
#         df[df["split"] == "dev"].to_parquet(dev_parquet_path)
#         df[df["split"] == "test"].to_parquet(test_parquet_path)

#         logger.info("Data processing finished!")


        

#     finally:
#        logger.info("closing dask client and cluster..")
#        client.close()
#        cluster.close()

# if __name__ == "__main__":
#     process_data()  # type: ignore
    
    
    
 
from abhishek.config_schemas.data_processing_config_schema import DataProcessingConfig
from abhishek.utils.config_utils import get_config, get_pickle_config,custom_instantiate
from abhishek.utils.gcp_utils import access_secret_version
from abhishek.utils.data_utils import get_raw_data_with_version
from hydra.utils import instantiate
from dask.distributed import Client, LocalCluster  
from pathlib import Path
from abhishek.utils.utils import get_logger
import dask.dataframe as dd
from abhishek.config_schemas.data_processing.dataset_cleaners_schema import DatasetCleanerManagerConfig
import gc
import os

def process_raw_data(
    df_partition: dd.core.DataFrame, dataset_cleaner_manager: DatasetCleanerManagerConfig
) -> dd.core.Series:
    processed_partition: dd.core.Series = df_partition["text"].apply(dataset_cleaner_manager)
    return processed_partition

@get_pickle_config(config_path="abhishek/configs/automatically_generated", config_name="data_processing_config")
def process_data(config: DataProcessingConfig) -> None: 
    
    
    # print("\n\n\nOkay\n\n")
    # my_secret = access_secret_version(cyberbullying-428016,abhishek-secret )
    # print(my_secret)
    # return

    # print(config)
    # print("\n\n\nOkay\n\n")
    # return
    
    
    logger = get_logger(Path(__file__).name)
    logger.info("Processing raw data..")
    
    processed_data_save_dir = config.processed_data_save_dir

    # for local dask cluster Increase the memory limit for each worker and enable spilling to disk
    # cluster = LocalCluster(memory_limit='4GB', processes=True, dashboard_address=None)  # Adjust as needed
  
        # for GCP  
    cluster = custom_instantiate(config.dask_cluster)
    
    client = Client(cluster)  
     
    try:
        dataset_reader_manager = instantiate(config.dataset_reader_manager)
        dataset_cleaner_manager = instantiate(config.dataset_cleaner_manager)
        
        df = dataset_reader_manager.read_data(config.dask_cluster.n_workers)
        
        # print(df.compute().head())
        # exit(0)
        
        logger.info("Cleaning data...")
        
        df = df.assign( 
            cleaned_text=df.map_partitions(
                process_raw_data,
                dataset_cleaner_manager=dataset_cleaner_manager,
                meta=("text", "object")
            )
        )
        df = df.compute()
        
        train_parquet_path = os.path.join(processed_data_save_dir, "train.parquet")
        dev_parquet_path = os.path.join(processed_data_save_dir, "dev.parquet")
        test_parquet_path = os.path.join(processed_data_save_dir, "test.parquet")
        
        # Filter and write the train dataset
        train_df = df[df["split"] == "train"]
        train_df.to_parquet(train_parquet_path)
        del train_df
        gc.collect()
        
        # Filter and write the dev dataset
        dev_df = df[df["split"] == "dev"]
        dev_df.to_parquet(dev_parquet_path)
        del dev_df
        gc.collect()
        
        # Filter and write the test dataset
        test_df = df[df["split"] == "test"]
        test_df.to_parquet(test_parquet_path)
        del test_df
        gc.collect()

        logger.info("Data processing finished!")
        docker_info = {"docker_image": config.docker_image_name, "docker_tag": config.docker_image_tag}
        docker_info_save_path = os.path.join(processed_data_save_dir, "docker_info.yaml")

        # write_yaml_file(docker_info_save_path, docker_info)
        with open_file(docker_info_save_path ,"w")as f:
            f.write(docker.info)
        logger.info("Data processing finished!")

    finally:
       logger.info("closing dask client and cluster..")
       client.close()
       cluster.close()

if __name__ == "__main__":
    process_data()  # type: ignore
