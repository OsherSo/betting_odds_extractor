import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

service = ChromeService(executable_path=ChromeDriverManager().install())


def get_data(links):
    li = []
    for link in links:
        driver = webdriver.Chrome(service=service)
        driver.get(link)

        games = driver.find_elements(by=By.CSS_SELECTOR, value="#tournamentTable .table-participant")

        odds = driver.find_elements(by=By.CSS_SELECTOR, value="#tournamentTable .odds-nowrp")
        odds = [odds[x:x + 3] for x in range(0, len(odds), 3)]

        data = pd.DataFrame({
            "Game": [item.text for item in games],
            "Home": [item[0].text for item in odds],
            "Draw": [item[1].text for item in odds],
            "Away": [item[2].text for item in odds],
        })
        li.append(data)

        driver.quit()

    result = pd.concat(li)
    result = result.reset_index(drop=True)
    return result


links_data = [
    "https://www.oddsportal.com/soccer/england/premier-league/",
    "https://www.oddsportal.com/soccer/israel/ligat-ha-al/"
]
print(get_data(links_data))
