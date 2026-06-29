import requests
import zipfile

url = input("Enter the repo link")
response = requests.get(url)
with open("../dataset/repo.zip", "wb") as f:
    f.write(response.content)

with zipfile.ZipFile("../dataset/repo.zip", "r") as zip_ref:
    zip_ref.extractall("../dataset")