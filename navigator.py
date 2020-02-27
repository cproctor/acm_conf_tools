class NavigatorMixin:
    """Reusable mixin with common Selenium operations
    """
    def get_submit_button(self):
        return self.browser.find_element_by_xpath('//input[@type="submit"]')

    def get_table_value(self, key_text):
        "When there's a key-value table"
        xpath = "//td[contains(text(), '{}')]/../td[2]".format(key_text)
        return self.browser.find_element_by_xpath(xpath).text

