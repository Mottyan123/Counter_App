import flet as ft
import asyncio
from multiprocessing import shared_memory
import time

control_data = shared_memory.SharedMemory(name="control_shm", create=True, size=5)
red_team_name_data = shared_memory.SharedMemory(name="red_team_name_shm", create=True, size=128)
blue_team_name_data = shared_memory.SharedMemory(name="blue_team_name_shm", create=True, size=128)

time.sleep(2) # monitor.pyが先に起動するまで待つ


def main(page: ft.Page):
    timer_text = ft.Text("2:00", size=75, color=ft.Colors.BLACK)
    red_score_text = ft.Text("0", size=100, color=ft.Colors.BLACK)
    blue_score_text = ft.Text("0", size=100, color=ft.Colors.BLACK)
    control_data.buf[1:2] = (0).to_bytes(1, 'little')
    control_data.buf[:1] = (120).to_bytes(1, 'little')
    counter = 120
    mode = 0
    flag = False
    running = False

    def mode_change(e):
        nonlocal counter, mode, flag
        mode = e.control.selected_index
        if mode == 0: # 手動
            flag = False
            timer_text.value = "2:00"
            counter = 120
            control_data.buf[1:2] = (0).to_bytes(1, 'little')
            control_data.buf[:1] = (120).to_bytes(1, 'little')
        elif mode == 1: # 自律
            flag = False
            timer_text.value = "1:00"
            counter = 60
            control_data.buf[1:2] = (0).to_bytes(1, 'little')
            control_data.buf[:1] = (60).to_bytes(1, 'little')
        else: # 調整
            flag = True
            timer_text.value = "0:30"
            counter = 30
            control_data.buf[1:2] = (0).to_bytes(1, 'little')
            control_data.buf[:1] = (30).to_bytes(1, 'little')
        page.update()

    def start_timer(e):
        nonlocal running
        running = True
        page.run_task(timer_task) # 非同期タスクの開始

    def stop_timer(e):
        nonlocal running
        running = False

    def reset_timer(e):
        nonlocal running, counter, flag
        running = False
        if mode == 0: # 手動
            flag = False
            timer_text.value = "2:00"
            counter = 120
            control_data.buf[1:2] = (0).to_bytes(1, 'little')
            control_data.buf[:1] = (120).to_bytes(1, 'little')
        elif mode == 1: # 自律
            flag = False
            timer_text.value = "1:00"
            counter = 60
            control_data.buf[1:2] = (0).to_bytes(1, 'little')
            control_data.buf[:1] = (60).to_bytes(1, 'little')
        else: # 調整
            flag = True
            timer_text.value = "0:30"
            counter = 30
            control_data.buf[1:2] = (0).to_bytes(1, 'little')
            control_data.buf[:1] = (30).to_bytes(1, 'little')
        page.update()

    def red_team_name_change(e):    
        red_team_name = e.control.value.encode('utf-8')
        red_team_name_data.buf[:len(red_team_name)] = red_team_name
        red_team_name_data.buf[len(red_team_name):] = b"\x00" * (128 - len(red_team_name))

    def blue_team_name_change(e):    
        blue_team_name = e.control.value.encode('utf-8')
        blue_team_name_data.buf[:len(blue_team_name)] = blue_team_name
        blue_team_name_data.buf[len(blue_team_name):] = b"\x00" * (128 - len(blue_team_name))

    def red_score_plus1(e):
        red_score_text.value = str(int(red_score_text.value) + 1)
        if int(red_score_text.value) > 99:
            red_score_text.value = "99"
        control_data.buf[2:3] = int(red_score_text.value).to_bytes(1, 'little')
        page.update()

    def red_score_minus1(e):
        red_score_text.value = str(int(red_score_text.value) - 1)
        if int(red_score_text.value) < 0:
            red_score_text.value = "0"
        control_data.buf[2:3] = int(red_score_text.value).to_bytes(1, 'little')
        page.update()

    def red_score_plus2(e):
        red_score_text.value = str(int(red_score_text.value) + 2)
        if int(red_score_text.value) > 99:
            red_score_text.value = "99"
        control_data.buf[2:3] = int(red_score_text.value).to_bytes(1, 'little')
        page.update()

    def red_score_minus2(e):
        red_score_text.value = str(int(red_score_text.value) - 2)
        if int(red_score_text.value) < 0:
            red_score_text.value = "0"
        control_data.buf[2:3] = int(red_score_text.value).to_bytes(1, 'little')
        page.update()

    def red_score_plus7(e):
        red_score_text.value = str(int(red_score_text.value) + 7)
        if int(red_score_text.value) > 99:
            red_score_text.value = "99"
        control_data.buf[2:3] = int(red_score_text.value).to_bytes(1, 'little')
        page.update()

    def red_score_minus7(e):
        red_score_text.value = str(int(red_score_text.value) - 7)
        if int(red_score_text.value) < 0:
            red_score_text.value = "0"
        control_data.buf[2:3] = int(red_score_text.value).to_bytes(1, 'little')
        page.update()

    def blue_score_plus1(e):
        blue_score_text.value = str(int(blue_score_text.value) + 1)
        if int(blue_score_text.value) > 99:
            blue_score_text.value = "99"
        control_data.buf[3:4] = int(blue_score_text.value).to_bytes(1, 'little')
        page.update()

    def blue_score_minus1(e):
        blue_score_text.value = str(int(blue_score_text.value) - 1)
        if int(blue_score_text.value) < 0:
            blue_score_text.value = "0"
        control_data.buf[3:4] = int(blue_score_text.value).to_bytes(1, 'little')
        page.update()

    def blue_score_plus2(e):
        blue_score_text.value = str(int(blue_score_text.value) + 2)
        if int(blue_score_text.value) > 99:
            blue_score_text.value = "99"
        control_data.buf[3:4] = int(blue_score_text.value).to_bytes(1, 'little')
        page.update()

    def blue_score_minus2(e):
        blue_score_text.value = str(int(blue_score_text.value) - 2)
        if int(blue_score_text.value) < 0:
            blue_score_text.value = "0"
        control_data.buf[3:4] = int(blue_score_text.value).to_bytes(1, 'little')
        page.update()

    def blue_score_plus7(e):
        blue_score_text.value = str(int(blue_score_text.value) + 7)
        if int(blue_score_text.value) > 99:
            blue_score_text.value = "99"
        control_data.buf[3:4] = int(blue_score_text.value).to_bytes(1, 'little')
        page.update()

    def blue_score_minus7(e):
        blue_score_text.value = str(int(blue_score_text.value) - 7)
        if int(blue_score_text.value) < 0:
            blue_score_text.value = "0"
        control_data.buf[3:4] = int(blue_score_text.value).to_bytes(1, 'little')
        page.update()

    def reset_red_score(e):
        red_score_text.value = "0"
        control_data.buf[2:3] = (0).to_bytes(1, 'little')
        page.update()

    def reset_blue_score(e):
        blue_score_text.value = "0"
        control_data.buf[3:4] = (0).to_bytes(1, 'little')
        page.update()

    async def timer_task():
        nonlocal counter, running, flag
        if not flag:
            count = 3
            flag = True
            while count > 0:
                timer_text.value = str(count)
                control_data.buf[1:2] = (1).to_bytes(1, 'little')
                control_data.buf[:1] = count.to_bytes(1, 'little')
                page.update()
                if not running:
                    break
                count -= 1
                await asyncio.sleep(1)
        while running:
            minutes = counter // 60
            seconds = counter % 60
            timer_text.value = f"{minutes}:{seconds:02d}"
            control_data.buf[1:2] = (0).to_bytes(1, 'little')
            control_data.buf[:1] = counter.to_bytes(1, 'little')
            page.update()
            if counter == 0:
                running = False
                break
            counter -= 1
            await asyncio.sleep(1)

    #******* UI設定 ********
    page.window.width = 1280
    page.window.height = 720
    page.spacing = 30
    page.padding = 20
    page.margin = 0
    page.bgcolor = ft.Colors.WHITE
    page.add(
        ft.Row( # タイマー表示
            spacing = 150,
            controls = [
                ft.Text("ゲームクロック", size=50, color=ft.Colors.BLACK),
                timer_text,
            ],
        ),
        ft.Row( # タイマー操作ボタン
            spacing = 20,
            controls = [
                ft.CupertinoSlidingSegmentedButton(selected_index=0, thumb_color=ft.Colors.BLUE, controls = [ft.Text("手動"), ft.Text("自律"), ft.Text("調整")], on_change=mode_change),
                ft.ElevatedButton("リセット", on_click=reset_timer, style=ft.ButtonStyle(shape=ft.CircleBorder(), padding=50, bgcolor=ft.Colors.RED, color=ft.Colors.BLACK)),
                ft.ElevatedButton("スタート", on_click=start_timer, style=ft.ButtonStyle(shape=ft.CircleBorder(), padding=50, bgcolor=ft.Colors.GREEN, color=ft.Colors.BLACK)),
                ft.ElevatedButton("ストップ", on_click=stop_timer, style=ft.ButtonStyle(shape=ft.CircleBorder(), padding=50, bgcolor=ft.Colors.YELLOW, color=ft.Colors.BLACK)),
            ],
        ),
        ft.Row( # チーム名入力
            spacing = 0,
            controls = [
                ft.TextField(label="青チーム名", width=1280/2-30, color=ft.Colors.BLACK, label_style=ft.TextStyle(color=ft.Colors.BLUE), on_change=blue_team_name_change),
                ft.TextField(label="赤チーム名", width=1280/2-30, color=ft.Colors.BLACK, label_style=ft.TextStyle(color=ft.Colors.RED), on_change=red_team_name_change),
            ],
        ),
        ft.Row( # スコア表示＋スコア操作ボタン
            spacing = 0,
            controls = [
                ft.Container( # 青フィールドの得点板
                    content = ft.Container(
                        content = ft.Row(
                            spacing = 35,
                            controls = [
                                ft.Column( # スコア表示＋リセットボタン
                                    spacing = 10,
                                    alignment = ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                                    controls = [
                                        blue_score_text,
                                        ft.ElevatedButton("リセット", on_click=reset_blue_score, style=ft.ButtonStyle(shape=ft.CircleBorder(), padding=50)),
                                    ],
                                ),
                                ft.Column( # スコア操作ボタン(1点)
                                    spacing = 10,
                                    alignment = ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                                    controls = [
                                        ft.IconButton(icon=ft.Icons.ARROW_DROP_UP, icon_size=80, on_click=blue_score_plus1),
                                        ft.Text("±1", size=40, color=ft.Colors.BLACK),
                                        ft.IconButton(icon=ft.Icons.ARROW_DROP_DOWN, icon_size=80, on_click=blue_score_minus1),
                                    ],
                                ),
                                ft.Column( # スコア操作ボタン(2点)
                                    spacing = 10,
                                    alignment = ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                                    controls = [
                                        ft.IconButton(icon=ft.Icons.ARROW_DROP_UP, icon_size=80, on_click=blue_score_plus2),
                                        ft.Text("±2", size=40, color=ft.Colors.BLACK),
                                        ft.IconButton(icon=ft.Icons.ARROW_DROP_DOWN, icon_size=80, on_click=blue_score_minus2),
                                    ],
                                ),
                                ft.Column( # スコア操作ボタン(7点)
                                    spacing = 10,
                                    alignment = ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                                    controls = [
                                        ft.IconButton(icon=ft.Icons.ARROW_DROP_UP, icon_size=80, on_click=blue_score_plus7),
                                        ft.Text("±7", size=40, color=ft.Colors.BLACK),
                                        ft.IconButton(icon=ft.Icons.ARROW_DROP_DOWN, icon_size=80, on_click=blue_score_minus7),
                                    ],
                                ),
                            ],
                        ),
                        padding = 0,
                        margin = 0,
                        bgcolor = ft.Colors.WHITE,
                    ),
                    padding = 15,
                    margin = 0,
                    bgcolor = ft.Colors.BLUE,
                    width = 1280/2-30,
                    height = 720/10*5-60,
                ),
                ft.Container( # 赤フィールドの得点板
                    content = ft.Container(
                        content = ft.Row(
                            spacing = 35,
                            controls = [
                                ft.Column( # スコア表示＋リセットボタン
                                    spacing = 10,
                                    alignment = ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                                    controls = [
                                        red_score_text,
                                        ft.ElevatedButton("リセット", on_click=reset_red_score, style=ft.ButtonStyle(shape=ft.CircleBorder(), padding=50)),
                                    ],
                                ),
                                ft.Column( # スコア操作ボタン(1点)
                                    spacing = 10,
                                    alignment = ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                                    controls = [
                                        ft.IconButton(icon=ft.Icons.ARROW_DROP_UP, icon_size=80, on_click=red_score_plus1),
                                        ft.Text("±1", size=40, color=ft.Colors.BLACK),
                                        ft.IconButton(icon=ft.Icons.ARROW_DROP_DOWN, icon_size=80, on_click=red_score_minus1),
                                    ],
                                ),
                                ft.Column( # スコア操作ボタン(2点)
                                    spacing = 10,
                                    alignment = ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                                    controls = [
                                        ft.IconButton(icon=ft.Icons.ARROW_DROP_UP, icon_size=80, on_click=red_score_plus2),
                                        ft.Text("±2", size=40, color=ft.Colors.BLACK),
                                        ft.IconButton(icon=ft.Icons.ARROW_DROP_DOWN, icon_size=80, on_click=red_score_minus2),
                                    ],
                                ),
                                ft.Column( # スコア操作ボタン(7点)
                                    spacing = 10,
                                    alignment = ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                                    controls = [
                                        ft.IconButton(icon=ft.Icons.ARROW_DROP_UP, icon_size=80, on_click=red_score_plus7),
                                        ft.Text("±7", size=40, color=ft.Colors.BLACK),
                                        ft.IconButton(icon=ft.Icons.ARROW_DROP_DOWN, icon_size=80, on_click=red_score_minus7),
                                    ],
                                ),
                            ],
                        ),
                        padding = 0,
                        margin = 0,
                        bgcolor = ft.Colors.WHITE,
                    ),
                    padding = 15,
                    margin = 0,
                    bgcolor = ft.Colors.RED,
                    width = 1280/2-30,
                    height = 720/10*5-60,
                ),
            ],
        ),
    )


if __name__ == "__main__":
    try:
        ft.app(main)
    finally:
        control_data.buf[4:5] = (1).to_bytes(1, 'little') # 終了フラグを立てる
        control_data.close()
        red_team_name_data.close()
        blue_team_name_data.close()
        control_data.unlink()
        red_team_name_data.unlink()
        blue_team_name_data.unlink()