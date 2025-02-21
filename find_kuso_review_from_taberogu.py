import requests
from bs4 import BeautifulSoup
import csv
import sys
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time

def get_reviews(url):
    options = Options()
    options.add_argument("--headless")  # ヘッドレスモード（GUIなしで実行）
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    
    # すべての「もっと見る」ボタンをクリック
    while True:
        try:
            more_buttons = driver.find_elements(By.CLASS_NAME, "rvw-showall-trigger__target")
            if not more_buttons:
                break
            for button in more_buttons:
                driver.execute_script("arguments[0].click();", button)
                time.sleep(2)  # ボタンが押された後、内容が更新されるまで待機
        except Exception as e:
            print(f"Error clicking 'もっと見る': {e}")
            break
    
    time.sleep(5)  # すべてのレビューが表示されるまで十分に待機
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    
    reviews = []
    review_items = soup.find_all("div", class_="rvw-item")
    for item in review_items:
        score_tag = item.select_one("b.c-rating-v3__val")
        review_at_container = item.select_one("div.rvw-item__date") or item.select_one("div.rvw-item__single-date")
        content_tag = item.select_one("div.rvw-item__rvw-comment")
        
        score = score_tag.text.strip() if score_tag else "N/A"
        
        # 訪問日時の取得（「訪問」「回目」は削除）
        if review_at_container:
            spans = review_at_container.find_all("span")
            visit_date = spans[0].text.strip().replace("訪問", "") if spans else "N/A"
        else:
            visit_date = "N/A"
        
        content = content_tag.text.strip() if content_tag else "N/A"
        
        reviews.append([score, visit_date, content])
    
    return reviews

def save_to_csv(reviews, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["score", "review_at", "content"])
        writer.writerows(reviews)
    print(f"Saved {len(reviews)} reviews to {filename}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python find_kuso_review_from_taberogu.py <tabelog_store_url>")
        return
    
    base_url = sys.argv[1]
    match = re.search(r'/([^/]+)/?$', base_url)
    store_id = match.group(1) if match else "unknown"
    
    now = datetime.now().strftime("%Y%m%d%H%M")
    filename = f"kuso_review_from_{store_id}_{now}.csv"
    
    reviews = get_reviews(base_url + "/dtlrvwlst/")
    if reviews:
        save_to_csv(reviews, filename)
    else:
        print("No reviews found.")

if __name__ == "__main__":
    main()
