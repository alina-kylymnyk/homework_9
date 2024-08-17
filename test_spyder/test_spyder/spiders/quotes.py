import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        for quote in response.css('div.quote'):
            # Зберігаємо дані про цитату
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('span small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }

            # Збираємо URL автора та переходимо на сторінку автора
            author_page = quote.css('span a::attr(href)').get()
            if author_page is not None:
                yield response.follow(author_page, self.parse_author)

        # Переходимо на наступну сторінку
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        # Зберігаємо дані про автора
        yield {
            'name': extract_with_css('h3.author-title::text'),
            'birthdate': extract_with_css('span.author-born-date::text'),
            'bio': extract_with_css('div.author-description::text'),
        }
