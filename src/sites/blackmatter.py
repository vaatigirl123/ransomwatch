from datetime import datetime
import logging

from bs4 import BeautifulSoup

from db.models import Victim
from net.proxy import Proxy
from .sitecrawler import SiteCrawler
import helpers.victims as victims
import helpers.pagination as pagination


class Blackmatter(SiteCrawler):
    actor = "Blackmatter"

    def handle_page(self, body: str):
        soup = BeautifulSoup(body, "html.parser")

        victim_list = soup.find_all("div", class_="col-post col-4 mb-3")

        for victim in victim_list:
            victim_name = victim.find("h4").text.strip()

            victim_leak_site = victim.find("div", class_="col-6 pl-1").find("a").attrs["href"]

            published_dt = datetime.now()

            victims.append_victims(self, victim_leak_site, victim_name, published_dt)
        self.session.commit()

    def scrape_victims(self):
        with Proxy() as p:
            pagination.handle_pages_for(self, p)
