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

    file_url = "https://tululu.org/txt.php?id=32168"
    file_name = "Peski_Marsa.txt"
    file_dir = os.getcwd()

    download_file(file_url, file_name, file_dir)


if __name__ == "__main__":
    main()
