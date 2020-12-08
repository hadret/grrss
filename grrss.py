# -*- coding: utf-8 -*-
"""Script for transforming 10 latest GitLab Release posts to RSS feed."""
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.request import urlopen
from xml.sax.saxutils import escape

# Provide the url_base and url_path for scrapping.
url_base = "https://about.gitlab.com"
url_path = "/blog/categories/releases/"

# Fetch the html, use bs4 for parsing and set date for now.
html = urlopen(url_base + url_path).read()
soup = BeautifulSoup(html, "html.parser")
now = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")


def get_item(a):
    """Do initial parsing of each article.

    This function is called from the print loop defined below and does basic
    variable assignment and transformation. While title and url are relatively
    straight forward, date has to be first transformed from a string to the
    date format so that strftime function can work.

    """
    article = a.select('a')[0]
    description = escape(a.select(".summary")[0].text.strip())
    title = escape(article.text.strip())
    url = url_base + article.attrs.get("href")

    created = a.select(".date")[0].text.strip()
    created = datetime.strptime(created, "%b %d, %Y")
    created = created.strftime("%a, %d %b %Y %H:%M:%S +0000")

    return """
    <item>
      <title>{0}</title>
      <link>{1}</link>
      <guid>{1}</guid>
      <description>{2}</description>
      <pubDate>{3}</pubDate>
    </item>
    """.format(title, url, description, created)


def print_items():
    """Spit out RSS feed with latest 10 posts."""
    print("""<?xml version="1.0" encoding="utf-8" ?>
    <rss version="2.0" xml:base="{0}" xmlns:dc="http://purl.org/dc/elements/\
1.1/" xmlns:atom="http://www.w3.org/2005/Atom">
      <channel>
        <title>GitLab Releases</title>
        <link>{0}{1}</link>
        <description>An unofficial RSS feed for GitLab Releases</description>
        <language>en</language>
        <atom:link href="https://hadret.com/rss/gitlab.xml" rel="self" \
type="application/rss+xml" />
        <generator>grrss - https://github.com/hadret/grrss</generator>
        <pubDate>{2}</pubDate>
    """.format(url_base, url_path, now))

    for a in soup.select('.article', limit=10):
        item = get_item(a)
        if item:
            print(item)

    print("""
        </channel>
    </rss>
    """)


print_items()
