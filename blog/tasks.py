import os

import feedparser


from celery import shared_task
from datetime import timedelta
from django.utils import timezone


from .models import *
from .utils import save_new_contents



# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after your job has run. You should use it
# to wrap any jobs that you schedule that access the Django database in any way.


def fetch_and_save(_feeds, content_model):
     print("Saving contents....")
     for feed_url in _feeds:
        _feed = feedparser.parse(feed_url)
        save_new_contents(_feed, content_model)


@shared_task
def fetch_crypto_content():
    """Fetches latest crypto contents"""
    _feeds = [
        "https://cointelegraph.com/rss", "https://bitcoinmagazine.com/.rss/full/", "https://bitcoinist.com/feed/",
        "https://newsbtc.com/feed/", "https://cryptopotato.com/feed/", "https://crypto.news/feed/",
        "https://hackernoon.com/tagged/cryptocurrency/feed", "https://blog.bitmex.com/feed/",
        "https://coincheckup.com/blog/feed/", "https://coinchapter.com/feed/",
        "https://coinjournal.net/feed/"
    ]
    fetch_and_save(_feeds, CryptoContent)



@shared_task
def fetch_tech_jobs():
    """Fetch latest tech job updates"""
    _feeds = [
        "constantrecruitment.co.uk/feed", "https://constantrecruitment.co.uk/feed/",
        "https://fabricstaffing.com/feed/", "https://www.codility.com/blog/",
        "https://recruitingdaily.com/category/hr-recruiting-technology/feed/", "https://www.edgetech.ai/feed/",
        "https://www.summeroftech.co.nz/blog?format=rss", "https://blog.honeypot.io/feed.xml",
        "https://www.codingame.com/work/feed/", "https://techcrunch.com/category/startups/feed/",
        "https://weworkremotely.com/categories/remote-back-end-programming-jobs.rss",
        "https://weworkremotely.com/categories/remote-full-stack-programming-jobs.rss",
        "https://weworkremotely.com/remote-jobs.rss", "https://www.indeed.com/rss?q=",
        "https://news.crunchbase.com/feed/", "https://joblistnigeria.com/feed",
        "https://www.jobzilla.ng/feed", "https://techcrunch.com/region/africa/feed/",
        "https://disrupt-africa.com/feed/", "https://ventureburn.com/category/startups/feed/",
    ]
    fetch_and_save(_feeds, JobUpdatesContent)


@shared_task
def fetch_cyber_content():
    """Fetches cyber security contents and news"""
    _feeds = [
        "https://latesthackingnews.com/feed", "https://feeds.feedburner.com/TheHackersNews",
        "https://www.darkreading.com/rss_simple.asp", "https://www.csoonline.com/index.rss",
        "https://www.threatpost.com/feed/", "https://krebsonsecurity.com/feed/",
        "https://www.scmagazine.com/rss/news/", "https://feeds.feedburner.com/Securityweek",
        "https://www.computerworld.com/index.rss", "https://www.cyberscoop.com/feed/",
        "https://www.eweek.com/security/feed/", "https://www.cyberdefensemagazine.com/feed/",
        "https://www.helpnetsecurity.com/feed/", "https://cybersecurityventures.com/feed/",
        "https://www.cybersecurity-insiders.com/feed/", "https://securityaffairs.co/feed",
        "https://securelist.com/feed/", "https://securityintelligence.com/feed/",
    ]
    fetch_and_save(_feeds, CyberSecurityContent)


@shared_task
def fetch_python_content():
    """Fetches pythonic contents"""
    _feeds = [
        "https://www.blog.pythonlibrary.org/feed/", "https://blog.finxter.com/feed/",
        "https://www.fullstackpython.com/feeds/all.atom.xml", "https://talkpython.fm/episodes/rss",
        "https://www.pythonpodcast.com/rss/", "https://feeds.feedburner.com/DougHellmann/",
        "https://planetpython.org/rss20.xml", "https://realpython.com/atom.xml?format=xml",
        "https://feeds.feedburner.com/PythonSoftwareFoundationNews", "https://blog.jetbrains.com/pycharm/feed/",
        "https://planet.scipy.org/feed.xml", "https://www.pythonblogs.com/feed/",
        "https://devblogs.microsoft.com/python/feed/", "https://blog.python.org/feeds/posts/default",
        "https://developers.redhat.com/taxonomy/term/12611/feed", "https://www.askpython.com/feed",
        "https://anvil.works/blog/feed.xml", "https://pythonguides.com/feed/",
        "https://blog.pythonanywhere.com/index.xml",
    ]
    fetch_and_save(_feeds, PythonContent)


@shared_task
def fetch_sd_content():
    """Fetches software development contents"""
    _feeds = ["https://www.itpro.com/software-development/feed", "https://www.techradar.com/rss/news/software",
              "https://sdtimes.com/feed/", "https://www.javaworld.com/index.rss", "eweek.com/feed",
              "https://www.developer-tech.com/feed", "feeds.feedburner.com/thenextweb", "theencrypt.com/feed",
              "https://www.techradar.com/rss/news/java", "https://feed.infoq.com/",
              "techmeme.com/feed.xml", "https://news.ycombinator.com/rss",
              "https://www.programmableweb.com/rss.xml", "https://martinfowler.com/feed.atom",
              "https://scand.com/company/blog/feed/", "https://www.geeksforgeeks.org/feed/",
              "https://www.pluralsight.com/blog.rss.xml", "https://feeds.feedburner.com/TheDailyWtf",
              "https://mobidev.biz/feed", "https://www.plutora.com/feed",
              ]
    fetch_and_save(_feeds, SoftwareDevelopmentContent)


@shared_task
def fetch_ui_ux_content():
    """Fetches UI contents"""
    _feeds = [
        "https://uxdesign.cc/feed", "https://uxplanet.org/feed", "https://www.smashingmagazine.com/feed/",
        "https://uxmovement.com/feed/", "https://uxdesignmastery.com/feed/", "https://feeds.feedburner.com/uxmovement",
        "https://www.smashingmagazine.com/categories/ux-design/index.xml", "https://nngroup.com/feed/rss",
        "https://www.uxpin.com/studio/blog/category/ux-design/feed/", "https://boxesandarrows.com/feed/",
        "https://www.fastcompany.com/section/ux-design/rss", "https://uxdesignweekly.com/feed/",
        "https://usabilitygeek.com/feed/", "https://www.webdesignerdepot.com/feed/",
        "https://webdesignernews.com/feed/", "https://uxmastery.com/feed/", "https://uxstudioteam.com/ux-blog/feed/",
        "https://uxtools.co/feed.xml", "https://www.fastcompany.com/section/ux-design/rss",
    ]
    fetch_and_save(_feeds, UiUxContent)


@shared_task
def fetch_mobile_pc_content():
    """Fetches news relating to mobile and pc devices & development"""
    _feeds = [
        "pcworld.com/index.rss", "gadgets.ndtv.com/rss/feeds", "ghacks.net/feed", "androidheadlines.com/feed",
        "droid-life.com/feed", "iphonehacks.com/feed", "igeeksblog.com/feed", "buildfire.com/blog",
        "https://android-developers.googleblog.com/feeds/posts/default",
        "https://developer.apple.com/news/rss/news.rss",
        "https://mobilesyrup.com/feed/", "https://www.androidcentral.com/feed",
        "https://www.pocketgamer.com/rss/", "https://9to5mac.com/feed/",
        "https://venturebeat.com/category/mobile/feed/",
        "https://www.androidpolice.com/feed/", "https://thenextweb.com/mobile/feed",
        "https://www.xda-developers.com/feed/", "https://tympanus.net/codrops/feed/",
    ]
    fetch_and_save(_feeds, MobilePcContent)


@shared_task
def fetch_general_content():
    """Fetches contents for ai , startups and other things"""
    _feeds = ["https://www.zdnet.com/topic/artificial-intelligence/rss.xml", "https://techcrunch.com/feed/",
              "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=19854910",
              "https://www.techcrunch.com/startups/feed/", "knowtechie.com/feed", "https://arstechnica.com/feed/",
              "https://www.venturebeat.com/feed/", "https://www.wired.com/feed/rss/", "https://www.cnet.com/rss/news/",
              "https://www.technologyreview.com/feed/", "https://syncedreview.com/category/ai/feed/",
              "https://www.theverge.com/rss/index.xml", "https://feeds.feedburner.com/RedmondPie",
              "https://www.kdnuggets.com/feed/rss2", "https://www.forbes.com/sites/forbestechcouncil/feed/?format=rss",
              "https://www.aitrends.com/feed/", "https://readwrite.com/feed/", "https://thenextweb.com/feed/",
              "https://www.analyticsinsight.net/category/artificial-intelligence/feed/",
              ]
    fetch_and_save(_feeds, GeneralContent)



