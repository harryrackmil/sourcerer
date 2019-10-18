from bs4 import BeautifulSoup
import requests

def get_soup(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    return soup