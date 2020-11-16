# -*- coding:utf-8 -*-
import tkinter
import tkinter.font
import tkinter.messagebox

# 横に並べる数
MAX_X = 10

# 縦に並べる数
MAX_Y = 20

# 表示する文字列
TEXT = "字zi80"

# 表示する文字のサイズ
FONT_SIZE = 15

# ウィンドウのサイズ
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600

# ボタンクリック時に呼び出す関数


def button_func(event):

    # イベントを発行したウィジェットを取得
    button = event.widget

    # ウィジェットの font の設定を取得
    font_name = button.cget("font")

    # フォントオブジェクトを取得
    fontobj = tkinter.font.nametofont(font_name)

    # フォントの設定を取得
    font = fontobj.actual()

    # そのフォントの名前をメッセージとして表示
    tkinter.messagebox.showinfo(
        font["family"],
        "そのフォントは" + font["family"] + "です"
    )


# メインウィンドウ作成
app = tkinter.Tk()
geostr = str(WINDOW_WIDTH) + "x" + str(WINDOW_HEIGHT)
app.geometry(geostr)

# 利用可能なフォントのタプルを作成
families = tkinter.font.families()

# 表示する位置
x = 0
y = 0

# 各ボタンの間隔
dx = WINDOW_WIDTH / MAX_X
dy = WINDOW_HEIGHT / MAX_Y

# フォントリストの添字
i = 0

# 作成したフォントのGC防止用
font_list = []

# TEXTを全フォントファミリーで表示
for family in families:

    # フォントを作成
    button_font = tkinter.font.Font(
        family=family,
        size=FONT_SIZE,
    )

    # フォントを指定してボタンを作成
    button = tkinter.Button(
        app,
        text=TEXT,
        font=button_font,
        width=10,
        height=1,
    )

    # 位置を調節して配置
    button.place(x=x*dx, y=y*dy)

    # ボタンのクリックをバインド
    button.bind("", button_func)

    # 位置を横にずらす
    x += 1
    if x >= MAX_X:
        # 横に並べ終わったら縦方向にずらす
        y += 1
        x = 0

    i += 1

    # 作成したフォントを覚えておく
    font_list.append(button_font)

# メインループ
app.mainloop()
