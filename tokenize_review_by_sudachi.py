import pandas as pd
from sudachipy import dictionary, tokenizer

# SudachiPyの設定（dict="full" を使用）
tokenizer_obj = dictionary.Dictionary(dict="full").create()
mode = tokenizer.Tokenizer.SplitMode.C  # 文単位で分割する

# CSVファイルを読み込む
file_path = "kuso_review_from_13008029_202502261127.csv"  # レビューのCSVファイル
df = pd.read_csv(file_path)

# 形態素解析を実施し、分割結果を追加
def tokenize_review(text):
    if pd.isna(text):
        return ""  # NaN対策
    tokens = [m.surface() for m in tokenizer_obj.tokenize(text, mode)]
    return " | ".join(tokens)  # トークンを "|" で結合して出力

df["tokenized_review"] = df["content"].astype(str).apply(tokenize_review)

# 結果をCSVに出力
output_file = "tokenized_reviews.csv"
df.to_csv(output_file, index=False, encoding="utf-8-sig")

print(f"分割処理完了！{output_file} に保存しました。")
