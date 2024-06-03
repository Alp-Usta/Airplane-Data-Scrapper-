from playwright.sync_api import sync_playwright
import pandas as pd


def scrape_airlines(page):
    airline_inner_text = page.locator('//div[@class="dt-tr"]').all()

    airline_list = []
    i = 0
    while i < len(airline_inner_text):
        airline_dict = {}

        if i < len(airline_inner_text):
            airline_dict['airline name'] = airline_inner_text[i].inner_text()
            print(airline_dict['airline name'])
        else:
            airline_dict['airline name'] = "blank"

        airline_list.append(airline_dict)
        i += 1

    return airline_list


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        base_url = "https://www.planespotters.net/airlines/"
        total_pages = 13
        for page_number in range(1, total_pages + 1):
            page.goto(f"{base_url}A/{page_number}", timeout=60000)
            print(f"Scraping page {page_number}...")

            airline_list = scrape_airlines(page)
            all_airline_list.extend(airline_list)

        browser.close()

        df = pd.DataFrame(all_airline_list)
        df.to_excel('airline_list.xlsx', index=False)
        df.to_csv('airline_list.csv', index=False)


if __name__ == "__main__":
    main()
