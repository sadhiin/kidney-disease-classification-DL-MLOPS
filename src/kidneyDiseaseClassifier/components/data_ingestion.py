import os
import zipfile
import tarfile
import shutil
import gdown
import subprocess
import opendatasets as od
from kidneyDiseaseClassifier import logger
from kidneyDiseaseClassifier.utils.common import get_size
from kidneyDiseaseClassifier.entity.config_entity import DataIngestionConfig


class DataIngestionGoogle:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_gdrive_data(self):
        """
        Fetch the data from Gdrive
        :return:
        """

        try:
            dataset_url = self.config.source_URL
            zip_download_dir = self.config.local_data_file
            os.makedirs("artifacts/data_ingestion/gdrive", exist_ok=True)
            logger.info(f"Downloading data from the {dataset_url} into {zip_download_dir} location")
            file_id = dataset_url.split('/')[-2]
            prefix = "https://drive.google.com/uc?/export=download&id="
            # gdown.download(prefix+file_id,zip_download_dir)
            gdown.download(prefix + file_id, zip_download_dir, resume=True)
            logger.info(f"Data has been downloaded at {zip_download_dir}")
        except Exception as e:
            logger.error(e)
            raise e

    def extractor(self):
        """
        zip_file_path: str path
        Extract zip file
        :return: None
        """
        unzip_path = self.config.extracted_dir
        os.makedirs(unzip_path, exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)
        logger.info(f"Successfully extract the file at {unzip_path}")


class DataIngestionKaggle:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_kaggle_data(self):
        """
        Download data publicly available from kaggle
        :return:
        """
        try:
            dataset_url = self.config.source_URL
            zip_download_dir = self.config.local_data_file
            os.makedirs("artifacts/data_ingestion/kaggle", exist_ok=True)
            logger.info(f"Downloading data from the {dataset_url} into {zip_download_dir} location")

            kaggle_api = read_yaml(KAGGLE_SECRET_FILE_PATH)

            os.environ["KAGGLE_USERNAME"] = kaggle_api.kaggle_username
            os.environ["KAGGLE_KEY"] = kaggle_api.kaggle_api_key

            command = f"kaggle datasets download {dataset_url.split('/datasets/')[-1]} -p {zip_download_dir} --unzip"

            subprocess.run(command.split())

        except Exception as e:
            raise e

    def get_newly_downloaded_file(self, directory: str):
        # Ensure the directory exists
        if not os.path.exists(directory) or not os.path.isdir(directory):
            return None

        # List all files in the directory
        files = os.listdir(directory)

        # Filter out directories (if any)
        files = [file for file in files if os.path.isfile(os.path.join(directory, file))]

        # Sort files by modification time in descending order
        files.sort(key=lambda x: os.path.getmtime(os.path.join(directory, x)), reverse=True)

        # Check if there are any files in the directory
        if not files:
            return None

        # Return the path to the latest file
        latest_file = os.path.join(directory, files[0])
        return latest_file

    def extractor(self):
        """
        zip_file_path: str path
        Extract zip file
        :return: None
        """
        try:

            unzip_path = self.config.extracted_dir
            compressed_file = self.get_newly_downloaded_file(self.config.local_data_file)
            os.makedirs(unzip_path, exist_ok=True)
            if not os.path.exists(compressed_file):
                raise FileExistsError(f"{compressed_file} doesn't exists. Make sure file exists")

            logger.info(f"{compressed_file} file extraction is started!")

            file_extension = os.path.splitext(compressed_file)[1].lower()
            # Handle zip files
            if file_extension == ".zip":
                with zipfile.ZipFile(compressed_file, 'r') as zip_ref:
                    zip_ref.extractall(unzip_path)
                logger.info(f"Successfully extract the file at {compressed_file}")
                # Delete the compressed file after extraction
                os.remove(compressed_file)

            elif file_extension in (".tar", ".gz", ".bz2"):
                with tarfile.open(compressed_file, "r") as tar_ref:
                    tar_ref.extractall(os.path.dirname(compressed_file))
                logger.info(f"Successfully extract the file at {compressed_file}")

                # Delete the compressed file after extraction
                os.remove(compressed_file)
        except Exception as e:
            raise e
