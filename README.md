# newgrounds-scraper
Gets a user's posts from newgrounds.com.
There are two methods exposed for use, `init()`, and `get_posts()`

```python
init(dir: str) -> None:
  # by default, the cache is created in the working directory, but you can specify a subdirectory to place the cache
  # if you are not using the cache or are fine with it in the working directory, you need not call this function
```
```python
get_posts(user: str, enable_cache: bool, max_posts: int):
  # user is the username of the user to get posts for
  # enable_cache should be enabled during testing; it saves a copy of the html response to reduce network load
  # max_posts determines the maximum posts to return, default is 5
```