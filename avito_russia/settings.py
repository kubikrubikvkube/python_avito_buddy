# -*- coding: utf-8 -*-

# Scrapy settings for avito_russia project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'avito_russia'

SPIDER_MODULES = ['avito_russia.spiders']
NEWSPIDER_MODULE = 'avito_russia.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'Mozilla/5.0 (Linux; Android 7.0; HUAWEI VNS-L23) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.80 Mobile Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 5

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 5
CONCURRENT_REQUESTS_PER_IP = 5

REDIRECT_ENABLED = False
COOKIES_ENABLED = True
COOKIES_DEBUG = False
REACTOR_THREADPOOL_MAXSIZE = 32
DOWNLOAD_TIMEOUT = 15

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
DEFAULT_REQUEST_HEADERS = {
    'Host': 'm.avito.ru',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/json;charset=utf-8',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': 1,
    'TE': 'Trailers',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache'
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
    'scrapy.spidermiddlewares.httperror.HttpErrorMiddleware': None
}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 1
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#   'scrapy.extensions.telnet.CloseSpider': None,
#
# }

# Configure item pipelines

#
ITEM_PIPELINES = {
    'avito_russia.pipelines.DetailedItemSaverPipeline': 0,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 15
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 0.5
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# We're disabling 'duplicate filtering' because we're parsing API and this is false alarm
DUPEFILTER_CLASS = 'scrapy.dupefilters.BaseDupeFilter'

# We want our exported data to be encoded in UTF-8
FEED_EXPORT_ENCODING = 'utf-8'

# Into log file
# LOG_FILE = 'avito_russia.log'

# We want redirect all stdout output to log file
LOG_STDOUT = True

# Enable memory debugging
MEMDEBUG_ENABLED = False

# For the sake of stability we need to implement request retry logic
RETRY_ENABLED = True
RETRY_TIMES = 50
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 429]
RETRY_PRIORITY_ADJUST = -1

# Implicitly set statistics collection class
STATS_CLASS = 'scrapy.statscollectors.MemoryStatsCollector'
STATS_DUMP = True

# For debug purposes telnet console should be enabled
TELNETCONSOLE_ENABLED = False
TELNETCONSOLE_USERNAME = 'scrapy'
TELNETCONSOLE_PASSWORD = 'scrapy'

API_KEY = "af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir"
MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_USER = "avito"
MONGO_PASSWORD = "avito"
MONGO_DATABASE_NAME = "avito"
GENDER_RESOLVER_HOST = "http://localhost:8080/name-resolver"
# MONGO_HOST = "rc1b-usoz1ekmbx6yb0pi.mdb.yandexcloud.net"
# MONGO_PORT = 27018
# MONGO_USER = "avito"
# MONGO_PASSWORD = "DNIalr93118"
# MONGO_DATABASE_NAME = "avito"
DROPPED_ITEMS_THRESHOLD = 99
BROKEN_ADS_THRESHOLD = 30

LOG_ENABLED = True
LOG_LEVEL = "INFO"
#LOG_FILE = "main.log"
PROXY_ENABLED = True
