import flet as ft

def main(page: ft.Page):
    # Максимально простой код
    page.add(ft.Text("Hello World!", size=50))

ft.app(target=main)