from elevenlabs.conversational_ai.conversation import ClientTools
from langchain_community.tools import DuckDuckGoSearchRun

from dotenv import load_dotenv
import os
import openai
import requests
from PIL import Image
from io import BytesIO


def searchWeb(parameters):
    query = parameters.get("query")
    results = DuckDuckGoSearchRun(query=query)
    return results

def save_to_txt(parameters):
    filename = parameters.get("filename")
    data = parameters.get("data")

    formatted_data = f"{data}"

    with open(filename, "a", encoding="utf-8") as file:
        file.write(formatted_data + "\n")

def create_html_file(parameters):
    filename = parameters.get("filename")
    data = parameters.get("data")
    title = parameters.get("title")

    formatted_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
    </head>
    <body>
        <h1>{title}</h1>
        <div>{data}</div>
    </body>
    </html>
    """
    with open(filename, "w", encoding="utf-8") as file:
        file.write(formatted_html)

def generate_image(parameters):
    prompt = parameters.get("prompt")
    filename = parameters.get("filename")
    size = parameters.get("size", "1024x1024")  # Default size
    save_dir = parameters.get("save_dir", "generated_images")

    os.makedirs(save_dir, exist_ok=True)
    filename = filename if filename.endswith(".png") else filename + ".png"
    file_path = os.path.join(save_dir, filename)

    load_dotenv()
    openai.api_key = "OPENAI_API_KEY" 

    client = openai.OpenAI()

    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size=size,
        quality="standard",
        n=1,
    )
    
    image_url = response.data[0].url
    print(response)
    
    img_response = requests.get(image_url)
    image = Image.open(BytesIO(img_response.content))
    image.save(file_path)






client_tools = ClientTools()
client_tools.register("searchWeb", searchWeb)
client_tools.register("saveToTxt", save_to_txt)
client_tools.register("createHtmlFile", create_html_file)
client_tools.register("generateImage", generate_image)

