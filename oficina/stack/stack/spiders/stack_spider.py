"""
Module Docstring
"""
import snoop
from scrapy import Spider
from scrapy.selector import Selector
from snoop import pp
from stack.items import StackItem


def type_watch(source, value):
    return f"type({source})", type(value)


snoop.install(watch_extras=[type_watch])


class StackSpider(Spider):
    name = "stack"
    allowed_domains = ["stackoverflow.com"]
    start_urls = [
        "https://stackoverflow.com/questions?pagesize=50&sort=newest",
    ]

    @snoop
    def parse(self, response):
        tit = response.css("div.s-post-summary--content > h3 > a::text").getall()
        lnk = response.css("div.s-post-summary--content > h3 > a").xpath("@href").getall()
        data = zip(tit, lnk)
        for i in data:
            results = {
                "title": i[0],
                "url": i[1],
            }
            yield results
