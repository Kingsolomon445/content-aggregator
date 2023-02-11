from io import BytesIO

import feedparser
import re
import html
import requests
from PIL import Image
from dateutil import parser
import os

from django.db import transaction

import logging

# Django
from django.core.management.base import BaseCommand
from django.conf import settings
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.db.models import Q

# Third Party
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

# Models
from blog.models import *

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "content_aggregator.settings")

CLEANR = re.compile('<.*?>')

logger = logging.getLogger(__name__)


def cleanhtml(raw_html):
    cleantext = re.sub(CLEANR, '', raw_html)
    return cleantext


def find_content_image(item):
    image_fields = ["media_content", "media_thumbnail", "links", "media_group", "enclosures", "image", "thumbnail"]
    for field in image_fields:
        if hasattr(item, field):
            value = getattr(item, field)
            if isinstance(value, list):
                for sub_field in value:
                    if isinstance(sub_field, dict) and "url" in sub_field:
                        url = sub_field["url"]
                        try:
                            response = requests.get(url, stream=True)
                            response.raise_for_status()
                            image = Image.open(BytesIO(response.content))
                            return url
                        except (requests.exceptions.HTTPError, IOError, Image.DecompressionBombWarning):
                            continue
                    elif isinstance(value, dict) and "url" in value:
                        url = value["url"]
                        try:
                            response = requests.get(url, stream=True)
                            response.raise_for_status()
                            image = Image.open(BytesIO(response.content))
                            return url
                        except (requests.exceptions.HTTPError, IOError, Image.DecompressionBombWarning):
                            continue
    return None


def save_new_contents(feed, Content):
    """Saves new contents to the database.

    Checks the content GUID against the contents currently stored in the
    database. If not found, then a new `Content` is added to the database.

    Args:
        feed: requires a feedparser object
    """

    try:
        content_title = feed.channel.get('title', 'Technology')
    except AttributeError:
        content_title = "Technology"

    counter = 0
    for item in feed.entries:
        try:
            if counter >= 3:
                break
            guid = item.get('guid', item.get('id', ''))
            if not Content.objects.filter(Q(guid=guid) | Q(link=item.get('link', item.get('url', '')))).exists():
                content_image = find_content_image(item)
                tzinfos = {"PDT": -25200, "PST": -28800}  # PDT and PST offsets in seconds
                pub_date = parser.parse(item.get('published', item.get('updated', '')), tzinfos=tzinfos)
                description = html.unescape(cleanhtml(item.get('description', item.get('summary', ''))))
                content = Content(
                    title=item.get('title', item.get('name', '')),
                    description=description,
                    pub_date=pub_date,
                    link=item.get('link', item.get('url', '')),
                    content_name=content_title,
                    guid=guid,
                    image=content_image,
                )
                content.save()
                counter += 1
        except Exception as e:
            print(f"An error occurred while saving the contents for {content_title}: {e}")


# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after your job has run. You should use it
# to wrap any jobs that you schedule that access the Django database in any way.
@util.close_old_connections
def fetch_users_content():
    users_with_feeds = MyFeedContent.objects.values_list('user', flat=True).distinct()
    for user in users_with_feeds:
        feeds = MyFeedContent.objects.filter(user=user).values_list('url', flat=True)
        if not feeds:
            continue
        for feed in feeds:
            if not feed:
                continue
            try:
                parsed_feed = feedparser.parse(feed)
                save_new_contents(parsed_feed, MyFeedContent)
            except Exception as e:
                print(f"An error occurred while fetching the feed for {feed}: {e}")


@util.close_old_connections
def fetch_crypto_content():
    """Fetches latest crypto contents"""
    _feeds = [
        "https://cointelegraph.com/rss", "https://bitcoinmagazine.com/.rss/full/", "https://bitcoinist.com/feed/",
        "https://newsbtc.com/feed/", "https://cryptopotato.com/feed/", "https://crypto.news/feed/",
        "https://hackernoon.com/tagged/cryptocurrency/feed", "https://blog.bitmex.com/feed/",
        "https://coincheckup.com/blog/feed/", "https://coinchapter.com/feed/",
        "https://coinjournal.net/feed/"
    ]
    for feed_url in _feeds:
        _feed = feedparser.parse(feed_url)
        save_new_contents(_feed, CryptoContent)


@util.close_old_connections
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
    for feed_url in _feeds:
        _feed = feedparser.parse(feed_url)
        save_new_contents(_feed, JobUpdatesContent)


@util.close_old_connections
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
    for feed_url in _feeds:
        _feed = feedparser.parse(feed_url)
        save_new_contents(_feed, CyberSecurityContent)


@util.close_old_connections
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
        "https://blog.pythonanywhere.com/index.xml", "https://pycon.blogspot.com/feeds/posts/default",
    ]
    for feed_url in _feeds:
        _feed = feedparser.parse(feed_url)
        save_new_contents(_feed, PythonContent)


@util.close_old_connections
def fetch_sd_content():
    """Fetches software development contents"""
    _feeds = ["https://www.itpro.com/software-development/feed", "https://www.techradar.com/rss/news/software",
              "https://sdtimes.com/feed/", "https://www.javaworld.com/index.rss", "eweek.com/feed",
              "https://www.developer-tech.com/feed", "feeds.feedburner.com/thenextweb", "theencrypt.com/feed",
              "https://www.techradar.com/rss/news/java", "https://feed.infoq.com/",
              "techmeme.com/feed.xml", "https://news.ycombinator.com/rss", "https://www.reddit.com/r/programming/.rss",
              "https://www.programmableweb.com/rss.xml", "https://martinfowler.com/feed.atom",
              "https://scand.com/company/blog/feed/", "https://www.geeksforgeeks.org/feed/",
              "https://www.pluralsight.com/blog.rss.xml", "https://feeds.feedburner.com/TheDailyWtf",
              "https://mobidev.biz/feed", "https://www.plutora.com/feed",
              ]
    for feed_url in _feeds:
        _feed = feedparser.parse(feed_url)
        save_new_contents(_feed, SoftwareDevelopmentContent)


@util.close_old_connections
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
    for feed_url in _feeds:
        _feed = feedparser.parse(feed_url)
        save_new_contents(_feed, UiUxContent)


@util.close_old_connections
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
    for feed_url in _feeds:
        _feed = feedparser.parse(feed_url)
        save_new_contents(_feed, MobilePcContent)


@util.close_old_connections
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
    for feed_url in _feeds:
        _feed = feedparser.parse(feed_url)
        save_new_contents(_feed, GeneralContent)


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """Deletes all apscheduler job execution logs older than `max_age`."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = 'Schedules jobs for fetching content from various websites'

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # Note that in production , the time interval shouldn't be in seconds , usually in hours , 6, 12 e.t.c
        scheduler.add_job(
            fetch_users_content,
            trigger="interval",
            minutes=1,
            id="Users Content",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job, Users Content.")

        # Schedule Cyber Security Content job to run every 1 minute
        scheduler.add_job(
            fetch_cyber_content,
            trigger="interval",
            minutes=1.1,
            id="CyberSecurity Contents",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job: The CyberSecurity Content.")

        # Schedule General Content job to run every 1 minute
        scheduler.add_job(
            fetch_general_content,
            trigger="interval",
            minutes=1.2,
            id="General Contents",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job: The General Content.")

        # Schedule Python Content job to run every 1 minute
        scheduler.add_job(
            fetch_python_content,
            trigger="interval",
            minutes=1.3,
            id="Python Contents",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job: The Python Content.")

        # Schedule Software Development Content job to run every 1 minute
        scheduler.add_job(
            fetch_sd_content,
            trigger="interval",
            minutes=1.4,
            id="SD Contents",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job: The Software Developments Content.")

        # Schedule Ui & Ux Content job to run every 1 minute
        scheduler.add_job(
            fetch_ui_ux_content,
            trigger="interval",
            minutes=1.5,
            id="UI Contents",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job: The UI Content.")

        # Schedule Mobile & Pc content job to run every 1 minute
        scheduler.add_job(
            fetch_mobile_pc_content,
            trigger="interval",
            minutes=1.6,
            id="Mobile & PC Contents",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job: The Mobile & PC Content.")

        # Schedule Job Updates content job to run every 1 minute
        scheduler.add_job(
            fetch_tech_jobs,
            trigger="interval",
            minutes=1.7,
            id="Job Updates & Contents",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job: The Job Updates & Contents.")

        # Schedule Crypto content job to run every 1 minute
        scheduler.add_job(
            fetch_crypto_content,
            trigger="interval",
            minutes=1.8,
            id="Crypto Contents",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job: The Crypto Contents.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="Delete Old Job Executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: Delete Old Job Executions.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
