# -*- coding: utf-8 -*-
from scrapy.spiders import XMLFeedSpider
from scrapy import Request
from outboundarticles.items import OutboundarticlesItem
from readability.readability import Document
import urlparse
from goose import Goose
import xml


class GooglealertsSpider(XMLFeedSpider):
    name = 'googlealerts'
    start_urls = [<Enter google alert url's here>]

    iterator = 'html'
    itertag = 'entry'

    def parse_node(self, response, node):
        i = OutboundarticlesItem()
        link_url = node.xpath('link/@href').extract()[0]
        urlparse_link = urlparse.urlparse(link_url)
        i['link'] = str(urlparse.parse_qs(urlparse_link.query)['url'][0])
        i['title'] = node.xpath('title/text()').extract()[0]
        i['description'] = node.xpath('content/text()').extract()[0]
        i['published'] = node.xpath('published/text()').extract()[0]
        request = Request(i['link'], callback=self.parse_rss_link)
        request.meta['item'] = i
        return request

    def parse_rss_link(self, response):
        item = response.meta['item']
        raw_html = response.body
        try:
            readability_prel = Document(raw_html).summary()
            item['article_content_readability'] = readability_prel
            #len(''.join(
            #    xml.etree.ElementTree.fromstring(readability_prel).itertext()))
        except:
            item['article_content_readability'] = ''
        try:
            g = Goose(config={'enable_image_fetching': False})
            article = g.extract(raw_html=raw_html)
            item['article_content_goose'] = article.cleaned_text
        except:
            item['article_content_goose'] = ''
        return item
