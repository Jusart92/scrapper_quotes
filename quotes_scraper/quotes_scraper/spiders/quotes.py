import scrapy
# Titulo = //h1/a/text()
# Citas = //span[@class="text" and @itemprop="text"text()]
# Top ten tags = //div[contains(@class,"tags-box")]//span[@class="tag-item"]/a/text()')
# Next pages button = //ul[@class="pager"]/li[@class="next"]/a/@href
# author = //div[@class="quote"]//small[@class="author"]/text()

class QuotesSpider(scrapy.Spider):
    #name can't be repeated
    name = 'quotes'
    start_urls=[
        'http://quotes.toscrape.com'
    ]
    custom_settings = {
        'FEED_URI': 'quotes.json',
        'FEED_FORMAT': 'json',
        'CONCURRENT_REQUESTS': 24,
        'MEMUSAGE_LIMIT_MB': 2048,
        'MEMUSAGE_NOTIFY_MAIL': ['jusart.92@gmail.com'],
        'ROBOTSTXT_OBEY': True,
        'USER_AGENT':'Arturo Juarez',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def parse_only_quotes(self, response, **kwargs):
        if kwargs:
            result = kwargs['quotes']

        quotes = response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall()
        authors = response.xpath('//div[@class="quote"]//small[@class="author"]/text()').getall()

        add_quotes =  list(map(lambda x,y:x+ 'by ' + y,quotes,authors))

        result.extend(add_quotes)

        next_page_button_link = response.xpath('//ul[@class="pager"]/li[@class="next"]/a/@href').get()
        if next_page_button_link: 
            yield response.follow(next_page_button_link, callback= self.parse_only_quotes, cb_kwargs={'quotes':result})
            #cb_kwargs   keyword arguments, diccionario para pasar argumentos a otra funcion
        else:
            yield{
                'quotes':result
            }

    def parse(self, response):
        # print('*' * 10)
        # print('\n\n\n')
        #print(response.status, response.headers)
        title = response.xpath('//h1/a/text()').get()
        # print (f'Titulo: {title}')
        # print('\n\n')
        
        quotes = response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall()
        # print('Citas')
        # for quote in quotes:
        #     print(f'- {quote}')
        #     print('\n')

        # print('\n\n')

        authors = response.xpath('//div[@class="quote"]//small[@class="author"]/text()').getall()

        result = list(map(lambda x,y:x+ ' by ' + y, quotes, authors))
        
        top_tags = response.xpath('//div[contains(@class,"tags-box")]//span[@class="tag-item"]/a/text()').getall()
        # print('Top ten tags')
        # for tag in top_tags:
        #     print(f'- {tag}')
        # print('\n\n\n')
        # print('*' * 10)
        top = getattr(self,'top',None)
        if top:
            top = int(top)
            top_tags = top_tags[:top]

        yield {
            'title': title,
            'top_tags': top_tags
        }

        next_page_button_link = response.xpath('//ul[@class="pager"]/li[@class="next"]/a/@href').get()
        if next_page_button_link: 
            yield response.follow(next_page_button_link, callback= self.parse_only_quotes, cb_kwargs={'quotes':result})
            #cb_kwargs   keyword arguments, diccionario para pasar argumentos a otra funcion