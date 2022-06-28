import json
from bs4 import BeautifulSoup
import requests

TEST_CACHE_FILE = "cache.html"
WORKING_CACHE_FILE = "cache.json"
DEFAULT_MAX_POSTS = 5

cached_posts = {}

def init(dir):
  global TEST_CACHE_FILE
  global WORKING_CACHE_FILE
  global cached_posts
  TEST_CACHE_FILE = dir + TEST_CACHE_FILE
  WORKING_CACHE_FILE = dir + WORKING_CACHE_FILE
  try:
    with open(WORKING_CACHE_FILE, "r") as f:
      print("Working Cache Found at " + WORKING_CACHE_FILE)
      cached_posts = json.loads(f.read())
  except FileNotFoundError:
    print("No working cache file, creating one now at " + WORKING_CACHE_FILE)
    with open(WORKING_CACHE_FILE, "x") as f:
      f.write(json.dumps(cached_posts))

def _write_wc_data():
  with open(WORKING_CACHE_FILE, "w") as f:
    f.write(json.dumps(cached_posts))

class _Post:
  def __init__(self, post_link: str, image_url:str, post_title:str):
    self.post_link = post_link
    self.image_url = image_url
    self.post_title = post_title
  def __str__(self) -> str:
    return self.post_title + '\n  ' + self.image_url + '\n  ' + self.post_link

def _create_cache_data(content):
  try:
    with open(TEST_CACHE_FILE, 'xb') as f:
      f.write(bytes(content, 'UTF-8'))
  except FileExistsError:
    print("Cache File already exists")

def _get_cache_data(url):
  try:
    with open(TEST_CACHE_FILE, 'rb') as f:
      print("Cache Found, reading from cache")
      return(str(f.read(), 'UTF-8'))
  except FileNotFoundError:
    print("No Cache, grabbing from web")
    url_content = str(requests.get(url).content, 'UTF-8')
    _create_cache_data(url_content)
    return url_content

def _get_url_data(url, enable_cache):
  if enable_cache:
    return _get_cache_data(url)
  else:
    return str(requests.get(url).content, 'UTF-8')

def _get_all_links(soup: BeautifulSoup):
  return soup.find_all("a")

def _process_post_link(a):
  title = str(a.h4.string)
  url = a['href']
  img_url = ''
  if cached_posts.get(url):
    print("getting " + title + " from disk")
    img_url = cached_posts[url]['image_url']
  else:
    print("getting " + title + " from web")
    url_content = str(requests.get(url).content, 'UTF-8')
    soup = BeautifulSoup(url_content, "html.parser")
    pod = soup.find('div', 'pod-body')
    img_url = pod.find('img')['src']
  new_post = _Post(url, img_url, title).__dict__
  cached_posts[url] = new_post
  return new_post

def get_posts(user: str, enable_cache: bool, max_posts: int = DEFAULT_MAX_POSTS) -> list[_Post]:
 # newgrounds has no easy way to get the extension of a file
 # currently assumes png, implement check_extensions later
 # or find a better way of grabbing extension

 #enable_cache = True
 url = "https://" + user + ".newgrounds.com/art/"
 url_content = _get_url_data(url, enable_cache)

 soup = BeautifulSoup(url_content, "html.parser")
 links = [x for x in _get_all_links(soup) if x.h4]
 posts = [_process_post_link(x) for x in links[:max_posts]]
 _write_wc_data()
 return posts