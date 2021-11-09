import os

import requests
from dotenv import load_dotenv


def download_file(url, filename, file_dir, params=None):
    response = requests.get(url, params)
    response.raise_for_status()

    file_path = os.path.join(file_dir, filename)

    with open(file_path, "wb") as file:
        file.write(response.content)


def main():
    load_dotenv()

    # dvmn_api_key = os.environ[""]

    dvmn_file_url = "https://dvmn.org/assets/img/logo.8d8f24edbb5f.svg"
    dvmn_file_name = "dvmn.svg"
    dvmn_file_dir = os.getcwd()

    download_file(dvmn_file_url, dvmn_file_name, dvmn_file_dir)


if __name__ == "__main__":
    main()
