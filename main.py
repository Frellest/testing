import flet as ft

def main(page: ft.Page):
    page.title = "Simple Test App"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.colors.WHITE
    
    page.add(
        ft.Column([
            ft.Text("Hello Flet!", size=30, color=ft.colors.BLACK),
            ft.Text("Если вы это видите - приложение работает", size=16, color=ft.colors.GREY_700),
            ft.ElevatedButton(
                "Тестовая кнопка",
                on_click=lambda e: print("Кнопка нажата!"),
                bgcolor=ft.colors.BLUE,
                color=ft.colors.WHITE
            )
        ])
    )

if __name__ == "__main__":
    ft.app(target=main)
