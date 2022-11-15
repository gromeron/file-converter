from locust import HttpUser, task
import os

headers = {}
filename = "./sample.mp3"

class Conversion(HttpUser):
    @task
    def convert(self):
        with open(filename, "rb") as f:
            form_data = {"format_select":"ogg"}
            #files = {"file":f}
            response = self.client.post(
                url="/upload",
                headers=headers,
                #files=files,
                timeout=10,
                data=form_data
            )