import requests
from bs4 import BeautifulSoup

def scrape_olx_car_covers(output_file="olx_car_covers.txt"):
    url = "https://www.olx.in/items/q-car-cover"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch page. Status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    # OLX listings are usually inside <li> or <div> with specific classes
    # This may change over time, so adjust selectors if needed
    listings = soup.find_all("li", {"data-aut-id": "itemBox"})

    results = []
    for item in listings:
        title_tag = item.find("span")
        link_tag = item.find("a", href=True)

        if title_tag and link_tag:
            title = title_tag.get_text(strip=True)
            link = "https://www.olx.in" + link_tag["href"]
            results.append(f"{title}\t{link}")

    # Save results to file
    with open(output_file, "w", encoding="utf-8") as f:
        for line in results:
            f.write(line + "\n")

    print(f"✅ Scraped {len(results)} results. Saved to {output_file}")

if __name__ == "__main__":
    scrape_olx_car_covers()
