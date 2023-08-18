import requests
import time
import urllib.request
from semantic_kernel.skill_definition import (
    sk_function,
    sk_function_context_parameter,
)
from semantic_kernel.orchestration.sk_context import SKContext


class ImagePlugin:
    @sk_function(
        description="Creates images with the given prompts",
        name="create_image_files",
        input_description="The content to be converted to images",
    )
    @sk_function_context_parameter(
        name="prompts",
        description="The content to be converted to images",
    )
    @sk_function_context_parameter(
        name="api_base",
        description="api_base",
    )
    @sk_function_context_parameter(
        name="api_key",
        description="api_key",
    )
    @sk_function_context_parameter(
        name="api_version",
        description="api_version",
    )
    def create_image_files(self, context: SKContext):
        api_base = context["api_base"]
        api_key = context["api_key"]
        api_version = context["api_version"]
        url = "{}dalle/text-to-image?api-version={}".format(api_base, api_version)
        headers= { "api-key": api_key, "Content-Type": "application/json" }
        images = []
        counter = 0
        image_list = []
        for phrase in context["prompts"]:
            print("Image for: ",phrase)
            body = {
                "caption": phrase ,
                "resolution": "1024x1024"
            }
            submission = requests.post(url, headers=headers, json=body)
            operation_location = submission.headers['Operation-Location']
            retry_after = submission.headers['Retry-after']
            status = ""
            #while (status != "Succeeded"):
            time.sleep(int(retry_after))
            response = requests.get(operation_location, headers=headers)
            status = response.json()['status']
            #print(status)
            if status == "Succeeded":
                counter += 1
                image_url = response.json()['result']['contentUrl']
                filename = "Images/file" + str(counter) + ".jpg"
                urllib.request.urlretrieve(image_url, filename)
                