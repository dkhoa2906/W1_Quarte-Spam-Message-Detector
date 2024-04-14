import requests

url = 'https://img2text-api-b33e78682724.herokuapp.com/'
image_path = '../demo.png'

with open(image_path, 'rb') as image_file:
    files = {'image': image_file}
    response = requests.post(url, files=files)
    print(response.text)
