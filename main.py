import flet as ft

def main(page: ft.Page):
    page.title = "Pyjnius Test"
    
    # Сначала проверяем доступность без блокировки интерфейса
    pyjnius_loaded = False
    try:
        # Быстрая проверка без полной загрузки
        import jnius
        pyjnius_loaded = True
    except:
        pyjnius_loaded = False
    
    if pyjnius_loaded:
        initial_status = "Pyjnius загружен - можно проверять"
        status_color = ft.colors.BLUE
    else:
        initial_status = "Pyjnius еще загружается - подождите и нажмите 'Проверить'"
        status_color = ft.colors.ORANGE
    
    status = ft.Text(initial_status, color=status_color)
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
            status.value = "❌ Ошибка Pyjnius"
            status.color = ft.colors.RED
            result_text.value = f"Ошибка: {ex}\n\nПопробуйте перезапустить приложение"
        
        page.update()
    
    page.add(ft.Column([
        status,
        ft.ElevatedButton("Проверить Pyjnius", on_click=check_pyjnius),
        result_text
    ]))

ft.app(target=main)
