import requests
import zipfile
import os

def create_zip_url(repo_url):
    repo_url = repo_url.rstrip("/")
    return repo_url + "/archive/refs/heads/main.zip"


def download_repo(repo_url:str, zip_path):
    
    if (repo_url.endswith(".zip")):
        zip_url = repo_url
    else :
        zip_url = create_zip_url(repo_url)

    response = requests.get(zip_url)

    if response.status_code != 200:
        raise Exception("Failed to download repository")

    with open(zip_path, "wb") as f:
        f.write(response.content)

    return zip_path


def extract_zip(zip_path, extract_to):

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_to)

    extracted_folder = os.listdir(extract_to)[0]

    repo_path = os.path.join(extract_to, extracted_folder)

    return repo_path