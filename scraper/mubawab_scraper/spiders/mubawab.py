import scrapy


class MubawabSpider(scrapy.Spider):
    name = "mubawab"
    allowed_domains = ["www.mubawab.ma"]
    start_urls = ["https://www.mubawab.ma/fr/st/marrakech/appartements-a-vendre"]

    def parse(self, response):
        listings = response.css('div.listingBox')
        # Si la page ne contient aucune annonce, on arrête la pagination ici
        if not listings:
            return
        

        for listing in listings:

            titre = listing.css('h2.listingTit a::text').get(default='').strip()

            if not titre:
                continue  # Skip listings without a title

            yield {
                'titre': listing.css('h2.listingTit a::text').get(default='').strip(),
                'lien': listing.css('h2.listingTit a::attr(href)').get(),
                'prix': listing.css('span.priceTag bdi::text').get(default='').strip(),
                'devise': listing.css('span.priceCurrency::text').get(default='').strip(),
                'localisation': ''.join(listing.css('span.listingH3::text').getall()).strip(),
                'description': listing.css('p.descLi::text').get(default='').strip(),
                'surface': listing.css('i.icon-triangle + span::text').get(default='').strip(),
                'pieces': listing.css('i.icon-house-boxes + span::text').get(default='').strip(),
                'chambres': listing.css('i.icon-bed + span::text').get(default='').strip(),
                'salle_de_bain': listing.css('i.icon-bath + span::text').get(default='').strip(),
                'features': listing.css('div.adFeature span.fSize12::text').getall(),
            }
        # Construire et suivre l'URL de la page suivante
        current_page = response.meta.get('page', 1)
        next_page = current_page + 1
        if next_page > 3:  # limite temporaire pour tester
            return
        
        next_url = f"{self.start_urls[0]}:p:{next_page}"


        yield scrapy.Request(
            url=next_url,
            callback=self.parse,
            meta={'page': next_page},
        )