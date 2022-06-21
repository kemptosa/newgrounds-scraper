from bs4 import BeautifulSoup
#from PIL import Image
import requests
#import imagehash

def get_posts(url, enable_cache, max_posts=5, check_extensions=[]):
 # newgrounds has no easy way to get the extension of a file
 # currently assumes png, implement check_extensions later
 # or find a better way of grabbing extension

 cachefile = "cache.html"
 #enable_cache = True

 urlcontent = ""

 if enable_cache:
  try:
   with open(cachefile, "rb") as f:
    print("Cache Found, reading from cache")
    urlcontent = f.read()
  except FileNotFoundError:
   print("No Cache, grabbing from web")
   urlcontent = requests.get(url).content
   with open(cachefile, "xb") as f:
    f.write(urlcontent)
 else:
  print("Cache Disabled, we do it live")
  urlcontent = requests.get(url).content
 #

 soup = BeautifulSoup(urlcontent, "html.parser")
 foundarray = ""

 for child in soup.find_all("script"):
  stch = str(child)
  itpos = stch.find("\"items\": [")
  if itpos != -1:

   #print(child)
   stchp = stch[itpos+9:]
   stchprbp = stchp.find("]")
   foundarray = stchp[:stchprbp+1].replace("\\n", "").replace("\\t", "").replace("\\", "")
 #

 arrsplit = foundarray.splitlines()
 numer = 0
 newsplit = []

 for line in arrsplit:
  if numer > 0:
   newsplit.append(line.strip()[1:-2])
  numer = numer + 1
 #
 print(urlcontent)
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
   ret_list.append([sshref, image_url, post_title])
  #snumer += 1
 return(ret_list[:max_posts])
#

print(get_posts("https://***REMOVED***.newgrounds.com/art/", True, 5, []))