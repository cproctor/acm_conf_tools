import yaml
import pickle 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from navigator import NavigatorMixin
from pathlib import Path
from parsing import *

class EasyChairScraper(NavigatorMixin):
    settings_file = "settings.yaml"
    secrets_file = "secrets.yaml"

    def __init__(self):
        with open(self.settings_file) as fh:
            settings = yaml.safe_load(fh)
        with open(self.settings_file) as fh:
            secrets = yaml.safe_load(fh)
        self.s = {**settings, **secrets}
        self.browser = self.get_browser()

    def get_submissions(self):
        submissions = []
        for url in self.get_submission_urls():
            submissions.append(self.parse_submission_url(url))
        return submissions

    def parse_submission_url(self, url):
        self.browser.get(url)
        authors = []
        author_rows = self.browser.find_elements_by_xpath("//table[@id='ec:table2']/tbody/tr")[2:]
        for row in author_rows:
            authors.append(self.parse_author_row(row))
        title = self.get_table_value("Title:")
        track = self.get_table_value("Track:")
        decision = self.get_table_value("Decision:")
        id = parse_submission_number(self.browser.find_element_by_class_name('pagetitle').text)
        submission = {
            "title": parse_title(title),
            "track": track,
            "id": id,
            "decision": decision,
            "authors": authors,
        }
        print(submission)
        return submission

    def parse_author_row(self, row):
        return {
            'first_name': row.find_element_by_xpath("./td[1]").text,
            'last_name': row.find_element_by_xpath("./td[2]").text,
            'email': row.find_element_by_xpath("./td[3]").text,
            'country': row.find_element_by_xpath("./td[4]").text,
            'organization': row.find_element_by_xpath("./td[5]").text,
        }

    def get_submission_urls(self):
        self.get_conference_index()
        xpath = "//table[@id='ec:table1']/tbody/tr/td[4]/a"
        elems = self.browser.find_elements_by_xpath(xpath)
        urls = [el.get_attribute('href') for el in elems]
        return urls

    def authenticate(self, force=False):
        self.browser.get(self.s['LOGIN_URL'])
        cookie_file = Path(self.s['COOKIES_PICKLE_FILE'])
        if not cookie_file.exists() or force:
            login = self.browser.find_element_by_id("name")
            login.send_keys(self.s['EASY_CHAIR_USERNAME'])
            pwd = self.browser.find_element_by_id("password")
            pwd.send_keys(self.s['EASY_CHAIR_PASSWORD'])
            self.get_submit_button().click()
            cookies = self.browser.get_cookies()
            for cookie in cookies:
                if cookie.get('expiry', None) is not None:
                    cookie['expires'] = cookie.pop('expiry')
            with open(self.s['COOKIES_PICKLE_FILE'], 'wb') as fh:
                pickle.dump(cookies, fh)
        else:
            with open(self.s['COOKIES_PICKLE_FILE'], 'rb') as fh:
                cookies = pickle.load(fh)
            for cookie in cookies:
                self.browser.add_cookie(cookie)
        
    def get_browser(self):
        return webdriver.Chrome()

    def get_submission_page(self, submission_id):
        url = self.s['SUBMISSION_URL'] + "?a={};submission={}".format(self.s['CONFERENCE_ID'], submission_id)
        self.browser.get(url)

    def get_conference_index(self):
        url = self.s['CONFERENCE_INDEX_URL'] + "?a={}".format(self.s['CONFERENCE_ID'])
        self.browser.get(url)

    def end(self):
        self.browser.close()


if __name__ == '__main__':
    ecs = EasyChairScraper()
    ecs.authenticate()
    with open("submissions.yaml", "w") as fh:
        fh.write(yaml.dump(ecs.get_submissions()))
    ecs.end()
    
        
