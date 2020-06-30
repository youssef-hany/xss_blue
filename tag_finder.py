from html.parser import HTMLParser
from urllib import parse

class TagFinder(HTMLParser):
    
    def __init__(self, base_url, page_url):
        super().__init__()
        self.base_url = base_url
        self.page_url = page_url
        self.links = set()
        self.formLinks = set()

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (attribute, value) in attrs:
                if attribute == 'href':
                    url = parse.urljoin(self.base_url, value)
                    self.links.add(url)
        if tag == 'input':

            for (attribute, value) in attrs:
                if attribute == 'type':
                    if value == 'submit':
                        url = parse.urljoin(self.base_url, self.page_url)
                        self.formLinks.add(url)

    def page_links(self):
        return self.links
 
    def page_form_links(self):
        return self.formLinks

    def error(self, message):
        pass

