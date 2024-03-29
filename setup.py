from setuptools import setup


setup(
    name='scrapy-strava',
    version='0.0.1',
    packages=['scrapy_strava', 'scrapy_strava.middlewares'],
    install_requires=['scrapy', 'oauthlib'],
    extras_require={
        'redis': ['redis', 'txredisapi', 'dj_redis_url']
    }
)