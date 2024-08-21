from playwright.sync_api import sync_playwright
import re


def openAndCloseBrowser(func):
    def wrapper():

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            pageData = func(page)

            browser.close()
            return pageData

    return wrapper


@openAndCloseBrowser
def parsePage(page):
    page.goto("https://www.snt-bugorok.ru/")
    data_parsing = page.text_content(".code")

    pattern = re.compile("'(\d+-\d+-\d+)',(\d+\.\d+)")
    price = re.findall(pattern, data_parsing)
    
    return price


