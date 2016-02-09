# -*- coding: utf-8  -*-

from datetime import datetime
from os.path import expanduser

from earwigbot.bot import Bot
from oursql import connect

__all__ = ["calculate_tif"]

def _get_db(bot):
    args = bot.config.wiki["_tifSQL"]
    args["read_default_file"] = expanduser("~/.my.cnf")
    args["autoping"] = True
    args["autoreconnect"] = True
    return connect(**args)

def _compute_stats(page, db):
    with db.cursor() as cursor:
        query = """SELECT COUNT(*) FROM templatelinks WHERE tl_title = ?
                   AND tl_namespace = 10 AND tl_from_namespace = 0"""
        cursor.execute(query, (page.title.replace(" ", "_"),))
        transclusions = cursor.fetchall()[0][0]

        # TODO
        tif = 0.0
        cache_time = None

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

    tif, transclusions, cache_time = _compute_stats(page, db)

    result["tif"] = tif
    result["transclusions"] = transclusions
    result["protection"] = page.protection
    if cache_time:
        result["cache_time"] = cache_time.strftime("%b %d, %Y %H:%M:%S UTC")
        result["cache_ago"] = _format_time(cache_time)
    return result
