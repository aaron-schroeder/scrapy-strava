from scrapy_strava.middlewares import StravaOAuth2Middleware
from scrapy_strava.middlewares import SimpleStravaRateLimitMiddleware


__all__ = ['StravaOAuth2Middleware', 'SimpleStravaRateLimitMiddleware']