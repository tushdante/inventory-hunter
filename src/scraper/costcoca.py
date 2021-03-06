from scraper.common import ScrapeResult, Scraper, ScraperFactory


class CostCoCAScrapeResult(ScrapeResult):
    def parse(self):
        alert_subject = 'In Stock'
        alert_content = ''

        # get name of product
        tag = self.soup.body.select_one('h1')
        if tag:
            alert_content += tag.text.strip() + '\n'
        else:
            self.logger.warning(f'missing title: {self.url}')

        # get listed price
        tag = self.soup.body.select_one('#pull-right-price')
        price_str = self.set_price(tag.getText())
        if price_str:
            alert_subject = f'In Stock for {price_str}'
        else:
            self.logger.warning(f'missing price: {self.url}')

        # check for add to cart button
        tag = self.soup.body.select_one('.primary-button-v2')
        if tag and 'add to cart' in str(tag).lower():
            self.alert_subject = alert_subject
            self.alert_content = f'{alert_content.strip()}\n{self.url}'


@ScraperFactory.register
class CostCoCAScraper(Scraper):
    @staticmethod
    def get_domain():
        return 'costco.ca'

    @staticmethod
    def get_driver_type():
        return 'selenium'

    @staticmethod
    def get_result_type():
        return CostCoCAScrapeResult
