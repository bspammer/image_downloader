from PIL import Image
from PIL.ImageFilter import GaussianBlur
from requests import get
import urllib
import sys

api_prefix = "https://api.500px.com/v1"
search_endpoint = "/photos/search"
rawoutputfile = "download_no_blur.jpg"
outputfile = "download.jpg"

if len(sys.argv) < 2:
    print("Usage: python script.py <searchterm> [photo index]")
    exit()
try:
    photo_index = int(sys.argv[2])-1
    photo_index = photo_index if photo_index >= 0 else 0
except IndexError:
    photo_index = 0
except ValueError:
    print("Invalid photo index")
    exit()

params = {
        "consumer_key": open("consumer_key").read(),
        "term": sys.argv[1],
        "image_size": 2048,
        "exclude": "Abstract,Animals,Black and White,Celebrities,Nude",
        "sort": "highest_rating"
    }

r = get(api_prefix + search_endpoint, params=params)
data = r.json()

photos = data.get("photos")
if photos is None or len(photos) == 0:
    print("No photos returned")
    exit()
try:
    images = photos[photo_index].get("images")
except IndexError:
    print("Not enough photos for specified index, using first photo instead")
    images = photos[0].get("images")
if images is None or len(images) == 0:
    print("No images for photo")
    exit()
url = images[0].get("url")
urllib.urlretrieve(url, filename=rawoutputfile)

im = Image.open(rawoutputfile)
w, h = im.size
crop = im.crop((70, h-210, 620, h-60))
blur = crop.filter(GaussianBlur(radius=9))
im.paste(blur, (70, h-210))
im.save(outputfile)
