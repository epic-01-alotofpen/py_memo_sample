import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

# メインウィンドウの設定
root = tk.Tk()
root.title("簡単メモ帳")
root.geometry("600x400")

# テキストエリアを作成
text_area = tk.Text(root, wrap='word')
text_area.pack(expand=1, fill='both')

# ファイルを新規作成する関数
def new_file():
    if messagebox.askokcancel("新規", "現在の内容を破棄して新規ファイルを作成しますか？"):
        text_area.delete(1.0, tk.END)

# ファイルを保存する関数
def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Text files", "*.txt"),
                                                        ("All files", "*.*")])
    if file_path:
        with open(file_path, 'w') as file:
            file.write(text_area.get(1.0, tk.END))
        messagebox.showinfo("保存", "ファイルが保存されました！")

# ファイルを開く関数
def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"),
                                                    ("All files", "*.*")])
    if file_path:
        with open(file_path, 'r') as file:
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, file.read())

# 検索機能の実装
def search_text():
    search_query = simpledialog.askstring("検索", "検索する文字列を入力してください:")
    if search_query:
        # すべてのハイライトをクリア
        text_area.tag_remove("highlight", "1.0", tk.END)

        start_pos = "1.0"
        while True:
            # テキストエリアで検索クエリを検索
            start_pos = text_area.search(search_query, start_pos, stopindex=tk.END)
            if not start_pos:
                break
            # 見つかった位置の終了位置を計算
            end_pos = f"{start_pos}+{len(search_query)}c"
            # ハイライトタグを追加
            text_area.tag_add("highlight", start_pos, end_pos)
            start_pos = end_pos
        # ハイライトの色を設定
        text_area.tag_config("highlight", background="yellow", foreground="black")



# メニューの作成
menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="新規", command=new_file)
file_menu.add_command(label="開く", command=open_file)
file_menu.add_command(label="保存", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="終了", command=root.quit)
menu_bar.add_cascade(label="ファイル", menu=file_menu)

# 検索メニューを追加
edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="検索", command=search_text)
menu_bar.add_cascade(label="編集", menu=edit_menu)

root.config(menu=menu_bar)

# アプリケーションのメインループ
root.mainloop()