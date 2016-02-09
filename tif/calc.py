# -*- coding: utf-8  -*-

from datetime import datetime, timedelta
from gzip import GzipFile
from json import loads
from os.path import expanduser
from StringIO import StringIO
from urllib import quote
from urllib2 import URLError

from earwigbot.bot import Bot
from oursql import connect

__all__ = ["calculate_tif"]

SITE_DB = "enwiki_p"

def _get_db(bot):
    args = bot.config.wiki["_tifSQL"]
    args["read_default_file"] = expanduser("~/.my.cnf")
    args["autoping"] = True
    args["autoreconnect"] = True
    return connect(**args)

def _count_transclusions(cursor, title):
    query = """SELECT COUNT(*)
        FROM {0}.templatelinks
        WHERE tl_title = ? AND tl_namespace = 10 AND tl_from_namespace = 0"""
    cursor.execute(query.format(SITE_DB), (title,))
    return cursor.fetchall()[0][0]

def _count_views(cursor, title):
    query = """SELECT SUM(cache_views), MIN(cache_time)
        FROM {0}.templatelinks
        INNER JOIN cache ON tl_from = cache_id
        WHERE tl_title = ? AND tl_namespace = 10 AND tl_from_namespace = 0"""
    cursor.execute(query.format(SITE_DB), (title,))
    return cursor.fetchall()[0]

def _get_avg_views(site, article):
    url = ("https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"
           "{0}.{1}/all-access/user/{2}/daily/{3}/{4}")
    days = 30
    slug = quote(article.replace(" ", "_"), safe="")
    start = datetime.utcnow().strftime("%Y%M%D")
    end = (datetime.utcnow() - timedelta(days=days)).strftime("%Y%M%D")
    query = url.format(site.lang, site.project, slug, start, end)

    try:
        response = site._opener.open(query)  # We're terrible
    except URLError:
        return None

    result = response.read()
    if response.headers.get("Content-Encoding") == "gzip":
        stream = StringIO(result)
        gzipper = GzipFile(fileobj=stream)
        result = gzipper.read()

    try:
        res = loads(result)
    except ValueError:
        return None

    if "items" not in res:
        return None
    return sum(item["views"] for item in res["items"]) / float(days)

def _update_views(cursor, site, title):
    cache_life = "7 DAY"
    query1 = """SELECT tl_from
        FROM {0}.templatelinks
        LEFT JOIN cache ON tl_from = cache_id
        WHERE tl_title = ? AND tl_namespace = 10 AND tl_from_namespace = 0 AND
            (cache_id IS NULL OR cache_time < DATE_SUB(NOW(), INTERVAL {1}))"""
    query2 = """INSERT INTO cache (cache_id, cache_views, cache_time)
            VALUES (?, ?, NOW()) ON DUPLICATE KEY
            UPDATE cache_views = ?, cache_time = NOW()"""

    cursor.execute(query1.format(SITE_DB, cache_life), (title,))
    while True:
        titles = cursor.fetchmany(1024)
        if not titles:
            break

        viewcounts = [(t, _get_avg_views(site, t)) for t in titles]
        parambatch = [(t, v, v) for (t, v) in viewcounts if v is not None]
        cursor.executemany(query2, parambatch)

def _compute_stats(db, page):
    title = page.title.replace(" ", "_")
    with db.cursor() as cursor:
        transclusions = _count_transclusions(cursor, title)
        _update_views(cursor, page.site, title)
        tif, cache_time = _count_views(cursor, title)
    return tif, transclusions, cache_time

def _format_time(cache_time):
    formatter = lambda n, w: "{0} {1}{2}".format(n, w, "" if n == 1 else "s")
    diff = datetime.utcnow() - cache_time
    if diff.seconds > 3600:
        return formatter(diff.seconds / 3600, "hour")
    if diff.seconds > 60:
        return formatter(diff.seconds / 60, "minute")
    return formatter(diff.seconds, "second")

def calculate_tif(title):
    bot = Bot(".earwigbot")
    db = _get_db(bot)
    site = bot.wiki.get_site()
    page = site.get_page(title)
    result = {"title": title, "page": page}

    if page.exists != page.PAGE_EXISTS:
        result["error"] = "no page"
        return result

    tif, transclusions, cache_time = _compute_stats(db, page)

    result["tif"] = tif
    result["transclusions"] = transclusions
    result["protection"] = page.protection
    if cache_time:
        result["cache_time"] = cache_time.strftime("%b %d, %Y %H:%M:%S UTC")
        result["cache_ago"] = _format_time(cache_time)
    return result
