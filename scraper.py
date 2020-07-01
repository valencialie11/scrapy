import scrapy

class YAnovels(scrapy.Spider):
    name = "YA_novels"
    start_urls = ['https://www.goodreads.com/list/show/25529.Best_Unknown_but_must_be_Known_books_']

    def parse(self, response):
        BOOKS_SELECTOR = '//tr'
        for YA_novels in response.xpath(BOOKS_SELECTOR):
            NAME_SELECTOR = './/span[contains(@aria-level, "4")]/text()'
            AUTHOR_SELECTOR = './/a[contains(@class, "authorName")]/span[contains(@itemprop, "name")]/text()'
            RATINGS_SELECTOR = './/span[contains(@class, "greyText smallText uitext")]/span[contains(@class, "minirating")]/text()'
            SCORE_SELECTOR = './/span[contains(@class, "smallText uitext")]/a[contains(@href, "#")]/text()'
            VOTES_SELECTOR = './/span[contains(@class, "smallText uitext")]/a[@id]/text()'
            IMAGE_SELECTOR = 'img ::attr(src)'
            yield{
                'Name': YA_novels.xpath(NAME_SELECTOR).extract_first(),
                'Author': YA_novels.xpath(AUTHOR_SELECTOR).extract_first(),
                'Ratings': YA_novels.xpath(RATINGS_SELECTOR).extract_first(),
                'Score': YA_novels.xpath(SCORE_SELECTOR).extract_first(),
                'Number of people who voted': YA_novels.xpath(VOTES_SELECTOR).extract_first(),
                'Image': YA_novels.css(IMAGE_SELECTOR).extract_first()
                #we just want the first element that matches the selector. This gives us a string, rather than a list of elements.
            }
        
            NEXT_PAGE_SELECTOR = './/a[@class= "next_page"]/@href'
            next_page = response.xpath(NEXT_PAGE_SELECTOR).extract()
            if next_page:
                next_href = next_page[0]
                next_page_url = 'https://www.goodreads.com' + next_href
                request = scrapy.Request(url=next_page_url)
                yield request