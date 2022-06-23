from typing import Literal
from bs4 import BeautifulSoup
#from PIL import Image
import requests
#import imagehash

CACHE_FILE = "cache.html"
DEFAULT_MAX_POSTS = 5

class Post:
  def __init__(self, post_link: str, image_url:str, post_title:str):
    self.post_link = post_link
    self.image_url = image_url
    self.post_title = post_title

def get_posts(user: str, enable_cache: bool, max_posts: int = DEFAULT_MAX_POSTS, check_extensions: list[Literal['.png', '.jpg', '.jpeg']] = ['.png']) -> list[Post]:
 # newgrounds has no easy way to get the extension of a file
 # currently assumes png, implement check_extensions later
 # or find a better way of grabbing extension

 #enable_cache = True
 url = "https://" + user + ".newgrounds.com/art/"
 url_content = ""

 if enable_cache:
  try:
   with open(CACHE_FILE, "rb") as f:
    print("Cache Found, reading from cache")
    url_content = str(f.read(), 'UTF-8')
  except FileNotFoundError:
   print("No Cache, grabbing from web")
   url_content = str(requests.get(url).content, 'UTF-8')
   with open(CACHE_FILE, "xb") as f:
    f.write(bytes(url_content, 'UTF-8'))
 else:
  print("Cache Disabled, we do it live")
  url_content = str(requests.get(url).content, 'UTF-8')
 #

 soup = BeautifulSoup(url_content, "html.parser")
 foundarray = ""

 for child in soup.find_all("a"):
  str(child)
 #

 arrsplit = foundarray.splitlines()
 numer = 0
 newsplit = []

 for line in arrsplit:
  if numer > 0:
   newsplit.append(line.strip()[1:-2])
  numer = numer + 1
 #

 newsplit.pop()
 newsplit[-1] = newsplit[-1] + ">"

 soup_split = []

 for line in newsplit:
   soup_split.append(BeautifulSoup(line, "html.parser"))
 #

 snumer = 0
 ret_list = []
 for small_soup in soup_split:
  if snumer == 0:
   sshref = small_soup.a["href"]
   thumbref = small_soup.a.div.img["src"]
   post_title = small_soup.a.div.img["alt"]
   split_ref = sshref.split("/")
   art_name = split_ref[-1]
   artist_name = split_ref[-2]
   image_url = thumbref.replace("thumbnails", "images").replace(".png", "_" + artist_name + "_" + art_name + ".png").split("?")[0]
   #im = Image.open(requests.get(image_url, stream=True).raw)
   #img_hash = imagehash.whash(im)
   
   new_post = Post(sshref, image_url, post_title)
   ret_list.append(new_post)
  #snumer += 1
 return(ret_list[:max_posts])
#
def a_sum():
  return 2
#