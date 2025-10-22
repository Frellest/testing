import flet as ft

def main(page: ft.Page):
    page.title = "Тестовое приложение"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    # Сначала создаем элементы
    status = ft.Text("Нажмите кнопку для теста", size=20)
    
    def test_notification(e):
        try:
            # Пробуем вызвать нативные уведомления
            page.invoke_method("createNotificationChannel")
            page.invoke_method("showNotification", {
                "title": "Тест",
                "message": "Уведомление работает!"
            })
            status.value = "✅ Уведомление отправлено"
        except Exception as ex:
            # Fallback - показываем диалог
            page.dialog = ft.AlertDialog(
                title=ft.Text("Тест уведомления"),
                content=ft.Text(f"Нативные уведомления недоступны: {ex}"),
                actions=[ft.TextButton("OK", on_click=lambda e: close_dialog())]
            )
            page.dialog.open = True
            status.value = "⚠️ Используется fallback уведомление"
        
        page.update()
    
    def close_dialog():
        page.dialog.open = False
        page.update()
    
    # Создаем кнопку после определения функции
    test_btn = ft.ElevatedButton("📢 Тест уведомления", on_click=test_notification)
    
    # Только ПОСЛЕ этого добавляем все на страницу
    page.add(
        ft.Column([
            ft.Text("Тестовое приложение", size=24, weight=ft.FontWeight.BOLD),
            status,
            test_btn,
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

if __name__ == "__main__":
    ft.app(target=main)
