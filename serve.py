from flask import Flask, render_template_string
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>World Energy Data</title>
  <style>
    .datatable-container { width:100%; overflow-x:auto; }
    table { border-collapse:collapse; width:100%; }
    th, td { padding:8px; border:1px solid #ccc; text-align:left; }
    th { background:#f2f2f2; }
  </style>
</head>
<body>
  <h1>World Energy Data (Live)</h1>
  {{ table_html|safe }}
</body>
</html>
"""

def fetch_table_html():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.worldometers.info/energy/")
    # Wait until table appears
    driver.implicitly_wait(10)
    el = driver.find_element(By.CSS_SELECTOR, ".datatable-container .datatable.datatable-table")
    html = el.get_attribute("outerHTML")
    driver.quit()
    return html

@app.route("/")
def home():
    try:
        table_html = fetch_table_html()
    except Exception as e:
        table_html = f"<p>Error fetching data: {e}</p>"
    return render_template_string(HTML_TEMPLATE, table_html=table_html)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)