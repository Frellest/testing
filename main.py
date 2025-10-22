import flet as ft

def main(page: ft.Page):
    page.title = "Тестовое приложение"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    def test_notification(e):
        try:
            page.invoke_method("createNotificationChannel")
            page.invoke_method("showNotification", {
                "title": "Тест",
                "message": "Уведомление работает!"
            })
            status.value = "✅ Уведомление отправлено"
        except Exception as ex:
            status.value = f"❌ Ошибка: {ex}"
        page.update()
    
    status = ft.Text("Нажмите кнопку для теста", size=20)
    
    page.add(
        ft.Column([
            ft.Text("Тестовое приложение", size=24, weight=ft.FontWeight.BOLD),
            status,
            ft.ElevatedButton("📢 Тест уведомления", on_click=test_notification),
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

if __name__ == "__main__":
    ft.app(target=main)
