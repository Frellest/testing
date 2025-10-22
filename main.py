import flet as ft

def main(page: ft.Page):
    page.title = "Pyjnius Test"
    
    status = ft.Text("Нажмите 'Проверить', когда Pyjnius загрузится", color=ft.colors.BLUE)
    result_text = ft.Text("")
    
    def check_pyjnius(e):
        try:
            from jnius import autoclass
            Build = autoclass('android.os.Build')
            Context = autoclass('android.content.Context')
            
            device_info = f"Устройство: {Build.MANUFACTURER} {Build.MODEL}\n"
            device_info += f"Android: {Build.VERSION.RELEASE}\n"
            device_info += f"Производитель: {Build.BRAND}"
            
            status.value = "✅ Pyjnius работает!"
            status.color = ft.colors.GREEN
            result_text.value = device_info
            
        except Exception as ex:
            status.value = "❌ Pyjnius еще не готов"
            status.color = ft.colors.RED
            result_text.value = f"Ошибка: {ex}\n\nПодождите немного и попробуйте снова"
        
        page.update()
    
    page.add(ft.Column([
        status,
        ft.ElevatedButton("Проверить Pyjnius", on_click=check_pyjnius),
        result_text
    ]))

ft.app(target=main)
