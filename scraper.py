import scrapy

class BrickSetSpider(scrapy.Spider):
    #BrickSetSpider is the subclass of the spider class provided by scrapy
    name = "brickset_spider"
    #Gave the spider name brickset_spider
    start_urls = ['http://brickset.com/sets/year-2016']

    def parse(self, response):
        SET_SELECTOR = '.set'
        for brickset in response.css(SET_SELECTOR):
            #when u inspect elements, each set is classified as class set. so to look for a class, we use .set in css
        
            #name of each set is within a h1
            NAME_SELECTOR = 'h1 ::text'
            # CSS pseudo-selector that fetches the text inside of the a tag rather than the tag itself.
            PIECES_SELECTOR = './/dl[dt/text() = "Pieces"]/dd/a/text()'
            MINIFIGS_SELECTOR = './/dl[dt/text() = "Minifigs"]/dd/a/text()'
            #We use XML because when we inspect the elements the 'pieces' and the actual number is in different tags
            IMAGE_SELECTOR = 'img ::attr(src)'
            yield{
                'Name': brickset.css(NAME_SELECTOR).extract_first(),
                #we just want the first element that matches the selector. This gives us a string, rather than a list of elements.
                'Number of pieces': brickset.xpath(PIECES_SELECTOR).extract_first(),
                'Number of minifigs': brickset.xpath(MINIFIGS_SELECTOR).extract_first(),
                'Image': brickset.css(IMAGE_SELECTOR).extract_first(),
            }
        
        NEXTPAGE_SELECTOR = '.next a ::attr(href)'
        next_page = response.css(NEXTPAGE_SELECTOR).extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )

            #The scrapy.Request is a value that we return saying “Hey, crawl this page”
            #callback=self.parse says “once you’ve gotten the HTML from this page, pass it back to this method so we can parse it, extract the data, and find the next page.“

