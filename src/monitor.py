import flet as ft
import asyncio
from multiprocessing import shared_memory

control_data = shared_memory.SharedMemory(name="control_shm", create=False)
red_team_name_data = shared_memory.SharedMemory(name="red_team_name_shm", create=False)
blue_team_name_data = shared_memory.SharedMemory(name="blue_team_name_shm", create=False)


def main(page: ft.Page):
    timer_text = ft.Text("0:00", size=175, color=ft.Colors.BLACK)
    red_score_text = ft.Text("0", size=350, color=ft.Colors.WHITE)
    blue_score_text = ft.Text("0", size=350, color=ft.Colors.WHITE)
    red_team_name = ft.Text(" チーム", size=75, color=ft.Colors.WHITE)
    blue_team_name = ft.Text(" チーム", size=75, color=ft.Colors.WHITE)

    #******* 通信タスク ********
    async def communication_task():
        mode = 0
        counter = 0
        red_team_name_raw = b""
        blue_team_name_raw = b""
        flag = 0
        while True:
            counter = int.from_bytes(control_data.buf[:1], 'little')
            mode = int.from_bytes(control_data.buf[1:2], 'little')
            red_score_text.value = str(int.from_bytes(control_data.buf[2:3], 'little'))
            blue_score_text.value = str(int.from_bytes(control_data.buf[3:4], 'little'))
            flag = int.from_bytes(control_data.buf[4:5], 'little')
            if flag == 1:
                page.window.close()
                break
            red_team_name_raw = bytes(red_team_name_data.buf[:]).split(b"\x00", 1)[0]
            blue_team_name_raw = bytes(blue_team_name_data.buf[:]).split(b"\x00", 1)[0]
            if mode == 0:
                minutes = counter // 60
                seconds = counter % 60
                timer_text.value = f"{minutes}:{seconds:02d}"
            else:
                timer_text.value = f"{counter}"
            red_team_name.value = f"{red_team_name_raw.decode('utf-8', errors='ignore')} チーム"
            blue_team_name.value = f"{blue_team_name_raw.decode('utf-8', errors='ignore')} チーム"
            page.update()
            await asyncio.sleep(0.01)

    #******* UI設定 ********
    page.window.full_screen = True
    page.padding = 0
    page.margin = 0
    page.spacing = 0
    page.add(
        ft.Container( # ゲームタイマー
            content = timer_text,
            padding = 0,
            margin = 0,
            alignment = ft.alignment.center,
            bgcolor = ft.Colors.WHITE,
            width = 1920,
            height = 1080 / 10 * 2.25,
        ),
        ft.Row( # 得点板
            spacing = 0,
            controls = [
                ft.Container( # 赤フィールドの得点板
                    content=ft.Container(
                        content = red_score_text,
                        padding = 0,
                        margin = 0,
                        alignment = ft.alignment.center,
                        bgcolor = ft.Colors.BLACK,
                    ),
                    padding = 35,
                    margin = 0,
                    bgcolor = ft.Colors.RED,
                    width = 1920 / 2,
                    height = 1080 / 10 * 6.25,
                ),
                ft.Container( # 青フィールドの得点板
                    content = ft.Container(
                        content = blue_score_text,
                        padding = 0,
                        margin = 0,
                        alignment = ft.alignment.center,
                        bgcolor = ft.Colors.BLACK,
                    ),
                    padding = 35,
                    margin = 0,
                    bgcolor = ft.Colors.BLUE,
                    width = 1920 / 2,
                    height = 1080 / 10 * 6.25,
                ),
            ],
        ),
        ft.Row( # チーム名表示
            spacing = 0,
            controls = [
                ft.Container( # 赤フィールドのチーム名表示
                    content = red_team_name,
                    padding = 10,
                    margin = 0,
                    alignment = ft.alignment.center,
                    bgcolor = ft.Colors.RED,
                    width = 1920 / 2,
                    height = 1080 / 10 * 1.5,
                ),
                ft.Container( # 青フィールドのチーム名表示
                    content = blue_team_name,
                    padding = 10,
                    margin = 0,
                    alignment = ft.alignment.center,
                    bgcolor = ft.Colors.BLUE,
                    width = 1920 / 2,
                    height = 1080 / 10 * 1.5,
                ),
            ],
        ),
    )

    page.run_task(communication_task) # communication_taskを非同期で実行


if __name__ == "__main__":
    try:
        ft.app(main)
    finally:
        control_data.close()
        red_team_name_data.close()
        blue_team_name_data.close()