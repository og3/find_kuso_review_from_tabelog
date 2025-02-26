import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys
import re

def get_menu(base_url):
    # 取得対象のメニューURL（料理・ドリンク・ランチ・コース）
    menu_urls = [
        "dtlmenu/",          # 料理メニュー
        "dtlmenu/drink/",    # ドリンクメニュー
        "dtlmenu/lunch/",    # ランチメニュー
        "party/"             # コースメニュー
    ]

    # 店舗IDを取得（URLの末尾の数字部分）
    store_id_match = re.search(r"/(\d+)/?$", base_url)
    store_id = store_id_match.group(1) if store_id_match else "unknown"

    # 取得したメニュー名を保存するリスト
    menu_items = []

    # 各メニューのページをスクレイピング
    for menu_url in menu_urls:
        full_url = base_url.rstrip("/") + "/" + menu_url  # スラッシュの処理
        try:
            # ページ取得
            response = requests.get(full_url, headers={"User-Agent": "Mozilla/5.0"})
            if response.status_code != 200:
                print(f"アクセス失敗: {full_url}")
                continue

            # HTMLをパース
            soup = BeautifulSoup(response.text, "html.parser")

            # メニュー名を取得
            menu_titles = soup.find_all("p", class_="rstdtl-menu-lst__menu-title")
            for title in menu_titles:
                menu_items.append(title.get_text(strip=True))

            print(f"取得完了: {full_url}")

        except Exception as e:
            print(f"エラー: {full_url} - {e}")

    # CSVに保存
    if menu_items:
        df = pd.DataFrame(menu_items, columns=["name"])
        output_file = f"menu_from_{store_id}.csv"
        df.to_csv(output_file, index=False, encoding="utf-8-sig")
        print(f"メニューをCSVに保存: {output_file}")
    else:
        print("メニューが取得できませんでした。")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("使い方: python scrape_menu.py [食べログの店舗URL]")
        sys.exit(1)
    
    base_url = sys.argv[1]
    get_menu(base_url)
