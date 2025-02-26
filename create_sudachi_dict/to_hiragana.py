import pandas as pd
import pykakasi

# ファイルのパス（適宜変更してください）
input_file = "ryori_dict.csv"  # 変換前のCSV
output_file = "ryori_dict_hiragana.csv"  # 変換後のCSV

# CSVを読み込む
df = pd.read_csv(input_file)

# `pykakasi` の初期化（漢字→ひらがな変換）
kakasi = pykakasi.kakasi()
kakasi.setMode("J", "H")  # 漢字をひらがなに変換
kakasi.setMode("K", "H")  # カタカナをひらがなに変換
converter = kakasi.getConverter()

# A列の存在を確認
if "表層形" in df.columns:
    # A列の単語をひらがな化してL列・M列に追加
    df["読み"] = df["表層形"].astype(str).apply(lambda x: converter.do(x))
    df["発音"] = df["読み"]  # M列にも同じデータを入れる
    
    # 変換後のCSVを保存
    df.to_csv(output_file, index=False, encoding="utf-8-sig")
    
    print(f"変換完了！保存しました: {output_file}")
else:
    print("エラー: A列が見つかりません。CSVのカラム名を確認してください。")
