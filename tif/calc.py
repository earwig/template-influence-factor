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

def _get_transclusions(page):
    # TODO
    yield page

def _get_view_average(page, db, cache_info):
    # TODO
    return 0.0

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
    template = site.get_page(title)
    result = {"title": title, "page": template}

    if template.exists != template.PAGE_EXISTS:
        result["error"] = "no page"
        return result

    tif = 0.0
    transclusions = 0
    cache_info = {"cache": False, "cache_time_raw": None}
    for page in _get_transclusions(template):
        tif += _get_view_average(page, db, cache_info)
        transclusions += 1

    if cache_info["cache"]:
        ctime = cache_info["cache_time"]
        cache_info["cache_time"] = ctime.strftime("%b %d, %Y %H:%M:%S UTC")
        cache_info["cache_ago"] = _format_time(ctime)

    result["tif"] = tif
    result["transclusions"] = transclusions
    result["protection"] = template.protection
    result.update(cache_info)
    return result
