import flet as ft
import threading

# ❌ НЕПРАВИЛЬНО - на верхнем уровне
# from jnius import autoclass

class AndroidManager:
    def __init__(self):
        self._jnius_loaded = False
        self._context = None
        
    def _load_jnius(self):
        """Загружаем Pyjnius в отдельном потоке"""
        try:
            from jnius import autoclass
            self.PythonActivity = autoclass('org.kivy.android.PythonActivity')
            self.Context = autoclass('android.content.Context')
            self._context = self.PythonActivity.mActivity
            self._jnius_loaded = True
            print("✅ Pyjnius загружен!")
        except Exception as e:
            print(f"❌ Ошибка Pyjnius: {e}")
    
    def init_async(self):
        """Инициализируем Pyjnius асинхронно"""
        if not self._jnius_loaded:
            threading.Thread(target=self._load_jnius, daemon=True).start()
    
    def send_notification(self, title, message):
        """Отправка уведомления (только если Pyjnius загружен)"""
        if not self._jnius_loaded:
            return False
            
        try:
            # Код уведомлений через Pyjnius
            NotificationManager = autoclass('android.app.NotificationManager')
            # ... остальной код
            return True
        except:
            return False

def main(page: ft.Page):
    page.title = "Pyjnius Test"
    
    android_mgr = AndroidManager()
    android_mgr.init_async()  # Запускаем в фоне
    
    status = ft.Text("Приложение запущено", size=20)
    
    def test_notification(e):
        if android_mgr.send_notification("Тест", "Сообщение"):
            status.value = "✅ Уведомление отправлено"
        else:
            status.value = "❌ Pyjnius ещё не готов"
        page.update()
    
    page.add(
        ft.Column([
            status,
            ft.ElevatedButton("Тест уведомления", on_click=test_notification),
            ft.Text("Pyjnius загружается в фоне...", size=12)
        ])
    )

ft.app(target=main)
