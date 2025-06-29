from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json

def fetch_energy_data():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)

    driver.get("https://www.worldometers.info/energy/")
    driver.implicitly_wait(10)
    container = driver.find_element(By.CSS_SELECTOR, ".datatable-container .datatable.datatable-table")
    rows = container.find_elements(By.CSS_SELECTOR, "tbody tr")
    
    data = []
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) >= 4:
            data.append({
                "country": cells[0].text.strip(),
                "energy_consumption_BTU": cells[1].text.strip(),
                "world_share": cells[2].text.strip(),
                "per_capita_yearly_BTU": cells[3].text.strip()
            })
    driver.quit()
    return data

if __name__ == "__main__":
    # Fetch and print JSON
    energy_data = fetch_energy_data()
    json_output = json.dumps(energy_data, indent=2)
    
    # Option 1: Save to a JSON file
    with open("energy_data.json", "w", encoding="utf-8") as f:
        f.write(json_output)
    
    # Option 2: Or just print it (for API use)
    # print(json_output)