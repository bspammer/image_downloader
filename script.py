from PIL import Image
from PIL.ImageFilter import GaussianBlur
from requests import get
import urllib
import sys

api_prefix = "https://api.500px.com/v1"
search_endpoint = "/photos/search"
outputfile = "download.jpg"

if len(sys.argv) < 2:
    print("Usage: python script.py <searchterm>")
    exit()

params = {
        "consumer_key": open("consumer_key").read(),
        "term": sys.argv[1],
        "image_size": 2048
    }

r = get(api_prefix + search_endpoint, params=params)
data = r.json()

photos = data.get("photos")
if photos is None or len(photos) == 0:
    print("No photos returned")
    exit()
images = photos[0].get("images")
if images is None or len(images) == 0:
    print("No images for photo")
    exit()
url = images[0].get("url")
urllib.urlretrieve(url, filename=outputfile)

im = Image.open(outputfile)
w, h = im.size
crop = im.crop((70, h-210, 620, h-60))
blur = crop.filter(GaussianBlur(radius=9))
im.paste(blur, (70, h-210))
im.save(outputfile)
