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
                '': YA_novels.xpath(SCORE_SELECTOR).extract_first(),
                'Number of people who voted': YA_novels.xpath(VOTES_SELECTOR).extract_first(),
                'Image': YA_novels.css(IMAGE_SELECTOR).extract_first()
                #we just want the first element that matches the selector. This gives us a string, rather than a list of elements.
            }
        
        NEXTPAGE_SELECTOR = './/a[contains(@class, "next_page")]/a[contains(@rel, "next")]/a[@href]'
        next_page = response.xpath(NEXTPAGE_SELECTOR).extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )
            #The scrapy.Request is a value that we return saying “Hey, crawl this page”
            #callback=self.parse says “once you’ve gotten the HTML from this page, pass it back to this method so we can parse it, extract the data, and find the next page.“