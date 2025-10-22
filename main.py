import flet as ft
import sys

def main(page: ft.Page):
    page.title = "Pyjnius Test"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.colors.WHITE
    
    # Пробуем импортировать Pyjnius
    try:
        from jnius import autoclass
        status = "✅ Pyjnius imported successfully"
        color = ft.colors.GREEN
    except Exception as e:
        status = f"❌ Pyjnius error: {str(e)}"
        color = ft.colors.RED
    
    page.add(
        ft.Column([
            ft.Text("Pyjnius Test", size=24, color=ft.colors.BLACK),
            ft.Text(status, size=16, color=color),
            ft.Text(f"Python: {sys.version}", size=12),
        ])
    )

ft.app(target=main)
