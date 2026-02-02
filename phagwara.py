from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

options = Options()
options.add_experimental_option("detach", True)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)
driver.get("https://www.google.com/maps/place/Phagwara+TechCADD+Basic+Computer+Course+%7C+Digital+Marketing+Course+%7C+Computer+Training+center+in+Phagwara/@31.2188378,75.7695139,17z/data=!4m8!3m7!1s0x391af55f3be8171f:0xad9cb9345374795f!8m2!3d31.2188378!4d75.7695139!9m1!1b1!16s%2Fg%2F11vzb1j9gw?hl=en&entry=ttu&g_ep=EgoyMDI2MDEyOC4wIKXMDSoASAFQAw%3D%3D")
wait = WebDriverWait(driver, 60)

# ---------- IMPROVED SCROLL REVIEWS ----------

scroll_div = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.m6QErb.DxyBCb.kA9KIf.dS8AEf")))

last_height = 0
same_height_count = 0

while True:
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_div)
    time.sleep(5)
    
    new_height = driver.execute_script("return arguments[0].scrollHeight", scroll_div)
    
    if new_height == last_height:
        same_height_count += 1
        if same_height_count >= 3:  # Wait for 3 consecutive same heights
            break
    else:
        same_height_count = 0
    
    last_height = new_height

# Extra wait after scrolling completes
time.sleep(5)

print("Scrolling completed")

# ---------- END SCROLL ----------

reviews = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".jftiEf.fontBodyMedium")))
print(f"Total reviews found: {len(reviews)}")

all_reviews = []

for data in reviews:
    try:
        name = data.find_element(By.CSS_SELECTOR, ".d4r55").text
    except:
        name = ""

    try:
        rating = data.find_element(By.CSS_SELECTOR, ".kvMYJc").get_attribute("aria-label")
    except:
        rating = ""

    try:
        time_txt = data.find_element(By.CSS_SELECTOR, ".rsqaWe").text
    except:
        time_txt = ""

    try:
        rev = data.find_element(By.CSS_SELECTOR, ".wiI7pd").text
    except:
        rev = ""

    all_reviews.append({
        "Name": name,
        "Rating": rating,
        "Time": time_txt,
        "Review": rev
    })

# ----------------- CREATE DATAFRAME -----------------
df = pd.DataFrame(all_reviews)

# ----------------- FIX TIME USING PANDAS -----------------
now = pd.Timestamp.now()

def convert_relative_time(x):
    if pd.isna(x) or x == "":
        return now

    x = x.lower()
    parts = x.split()

    if "hour" in x:
        n = int(parts[0]) if parts[0].isdigit() else 1
        return now - pd.Timedelta(hours=n)

    if "day" in x:
        n = int(parts[0]) if parts[0].isdigit() else 1
        return now - pd.Timedelta(days=n)

    if "week" in x:
        n = int(parts[0]) if parts[0].isdigit() else 1
        return now - pd.Timedelta(weeks=n)

    if "month" in x:
        n = int(parts[0]) if parts[0].isdigit() else 1
        return now - pd.Timedelta(days=n * 30)

    if "year" in x:
        n = int(parts[0]) if parts[0].isdigit() else 1
        return now - pd.Timedelta(days=n * 365)

    return now

df["Review_Date"] = df["Time"].apply(convert_relative_time)

# Sort latest first
df = df.sort_values("Review_Date", ascending=False)
df = df.drop(columns=["Review_Date"])
# ----------------- SAVE TO EXCEL -----------------
df.to_excel("phagwara_reviews.xlsx", index=False)


print("✅ Excel file created: phagwara_reviews.xlsx")

driver.quit()

