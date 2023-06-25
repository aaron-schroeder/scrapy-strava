# scrapy-strava

> Tools for downloading data from the Strava API with scrapy

## Installation
```
pip install git+https://github.com/aaron-schroeder/scrapy-strava.git
```

## Usage
Within your scrapy project's `settings.py`
```python
DOWNLOADER_MIDDLEWARES = {
   "scrapy_strava.middlewares.oauth.OAuth2Middleware": 543,
   "scrapy_strava.middlewares.ratelimit.SimpleStravaRateLimitMiddleware": 544,
}
```
If you use `SimpleStravaRateLimitMiddleware`, allow your spider to handle the
accompanying 429 HTTP status code.
```python
class MySpider(scrapy.Spider):
   # ...
   handle_httpstatus_list = [429, ...]
   # ...
```

## Dev

### Setup
```
git clone https://github.com/aaron-schroeder/scrapy-strava.git
pip install -e .
```

### Testing
```
python -m unittest discover tests
```
