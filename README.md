# find_kuso_review_from_taberogu
『食べログ』に掲載されている店のURLを渡すとその店の口コミを取得するスクリプト

## 仕様
- 『食べログ』の店の個別ページからすべてのレビューを取得する。
```
# 店の個別ページ（口コミ一覧画面）の例
http://tabelog.com/tokyo/A1323/A132305/13289424/dtlrvwlst/
```
- 取得する値とclassは以下の通り
```
- score(５段階評価のアレ）：<b class="c-rating-v3__val c-rating-v3__val--strong rvw-item__ratings--val">4.5</b>
- review_at（レビューが書かれた時間）：<div class="rvw-item__single-date">
- content（レビューの内容）：<div class="rvw-item__rvw-comment rvw-item__rvw-comment--custom">
```
- 取得した値はCSVに出力する(ファイル名の数字はURLの末尾と実行年月日時間分) 
```
# 出力例
ファイル名：kuso_review_from_13289424_202502210944.csv

score,review_at,content
4.5,2024/04訪問,本気で最高でした！炭火の近くのカウンターは少し火が近いのでホカホカする。すごい臨場感。炭火で焼いたホカホカのお魚は、家で焼くのと一味も二味も違う！フワフワなんだよぉ！お酒も喉を鳴らして飲みたくなるような、美味しい料理✨品のある店内は、デートにも、会食にも、あらゆる場面に使えそうノドグロ焼いてもらったんだけれど、こんな新鮮で、この価格でたべれるなんて、凄すぎる。絶対リピート確実です！
```
### 実行例
```bash
python find_kuso_review_from_taberogu.py http://tabelog.com/tokyo/A1323/A132305/13289424
```
