from storage.abc_storage import storage
import requests

class web_storage(storage):
    __API_KEY = ''
    
    def file_download(self, dir, url) -> None:
        with open(dir, "wb") as file:
            response = requests.get(url)
            file.write(response.content)
    
    def file_upload(self, dir) -> str:
        res = requests.post("e",
                files={"file":open(dir, "rb")}, data={"apiKey" : web_storage.__API_KEY})
        return res.json()['url']