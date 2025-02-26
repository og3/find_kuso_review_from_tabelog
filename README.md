## 食べログからレビューを取得してスコアリングするツール集
　食べログからレビューを取得して、形態素解析をした後で、文章が具体的であれば「良いレビュー」、抽象的で感情的なら「クソレビュー」として分類するためのツール集。
### 下準備
　食べログのレビューを正しく形態素解析できるように分割するsudachipyのユーザー辞書と、「良いレビュー」に点数をつけるための判定用辞書を用意する。
#### 食べログの店の個別ページからメニュー一覧を取得してCSVにする
　引数は食べログの個別ページ。
```bash
python find_menu/scrape_menu.py https://tabelog.com/tokyo/A1312/A131204/13270018
```
#### sudachipyの下準備編
　sudachipyのデフォルト辞書では、料理名をばらばらに分割してしまい、そのレビューが評価している料理名を正しく認識できない。
　これではレビューをスコアリングできないので、その店にある料理名を崩さずに形態素解析ができるようにする。
##### 取得したメニューをsudachipyの辞書フォーマットに入れる(要スクリプト化)
　以下のフォーマットの「表層形」に取得したメニューを入れる。
```csv
表層形,左文脈ID,右文脈ID,コスト,品詞,品詞細分類1,品詞細分類2,品詞細分類3,活用型,活用形,原形,読み,発音

```
　その他のカラムに入れる値は以下を参照。
https://github.com/og3/find_kuso_review_from_tabelog/issues/7
##### 「読み」、「発音」の欄が空なので「表層形」の値をひらがな化する(ファイルパスを良い感じに自動化する)
```bash
python create_sudachi_dict/to_hiragana.py
```
##### 作った辞書をsudachipyで使えるようにする
　SudachiPyでユーザー辞書を登録する
```bash
sudachipy ubuild -o user_dict.csv user_dict.dic
```
user_dict.csv → 作成したCSV辞書
user_dict.dic → 辞書ファイル（このファイルをSudachiPyに設定）

SudachiPyでユーザー辞書を適用
```python
from sudachipy import tokenizer, dictionary

tokenizer_obj = dictionary.Dictionary("user_dict.dic").create()
```
　ここまでで、sudachipyで料理名を崩さずに形態素解析ができるようになる。
#### スコアリングの下準備編
　「良いレビュー」のスコアリングは、以下の基準で行う。
```
・良い料理の評価：「料理名」、「値段」、「食べ物としての特徴（味や触感）」、「商品としての特徴（見た目や量）」、「評価（満足感）」があること。
・良い店の評価：「設備」、「特徴」、「評価」
```
　形態素解析で抜き出した文字列の中に、これらの項目があればポイントを振っていき、ポイントが高ければ「良いレビュー」とする。
##### 取得したメニューの一覧を配列のファイルを作る
　csvとto_aするようなイメージで作る(wip)
##### 食べ物の特徴を取得して配列で持つ
　以下のサイトから「用語」を取得し、配列にしてファイルを持つ。
https://www.naro.affrc.go.jp/org/nfri/yakudachi/terms/texture.html
　見た目の特徴は以下のサイトから取得して、同じくファイルで持つ。
https://note.com/fortunefactory/n/nc9cd30d3c862
### 食べログのレビューを評価する
#### 食べログの「口コミ」を取得する
#### 取得した「口コミ」をsudachipyで形態素解析する