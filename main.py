import flet as ft
import time
import json
from datetime import datetime

class NativeNotification:
    def __init__(self, page):
        self.page = page
    
    def show_notification(self, title, message):
        """Вызов нативного уведомления через Platform Channel"""
        try:
            # Создаем канал если не создан
            self.page.invoke_method("createNotificationChannel")
            
            # Показываем уведомление
            self.page.invoke_method(
                "showNotification",
                {
                    "title": title,
                    "message": message
                }
            )
            return True
        except Exception as e:
            print(f"Ошибка уведомления: {e}")
            # Fallback - показываем диалог
            self.show_fallback_notification(title, message)
            return False
    
    def show_fallback_notification(self, title, message):
        """Запасной вариант если нативные уведомления не работают"""
        self.page.dialog = ft.AlertDialog(
            title=ft.Text(title),
            content=ft.Text(message),
            actions=[ft.TextButton("OK", on_click=lambda e: self.close_dialog())]
        )
        self.page.dialog.open = True
        self.page.update()
    
    def close_dialog(self):
        self.page.dialog.open = False
        self.page.update()

class VoiceRecorder:
    """Запись голоса через Flet Audio"""
    
    def __init__(self, page):
        self.page = page
        self.is_recording = False
        self.audio_recorder = ft.AudioRecorder(
            on_state_changed=self.on_recording_state_change,
            on_result=self.on_recording_result
        )
        page.overlay.append(self.audio_recorder)
    
    def start_recording(self):
        """Начать запись"""
        try:
            self.audio_recorder.record()
            self.is_recording = True
            return True
        except Exception as e:
            print(f"Ошибка записи: {e}")
            return False
    
    def stop_recording(self):
        """Остановить запись"""
        try:
            self.audio_recorder.stop()
            self.is_recording = False
            return True
        except Exception as e:
            print(f"Ошибка остановки: {e}")
            return False
    
    def on_recording_state_change(self, e):
        print(f"Состояние записи: {e.data}")
    
    def on_recording_result(self, e):
        if e.data and e.data != "null":
            print(f"Запись сохранена: {e.data}")

class ReminderManager:
    """Управление напоминаниями"""
    
    def __init__(self, notification_manager):
        self.notification_manager = notification_manager
        self.reminders = []
        self.load_reminders()
        self.start_checker()
    
    def load_reminders(self):
        """Загрузка напоминаний"""
        try:
            with open("reminders.json", "r", encoding="utf-8") as f:
                self.reminders = json.load(f)
        except:
            self.reminders = []
    
    def save_reminders(self):
        """Сохранение напоминаний"""
        try:
            with open("reminders.json", "w", encoding="utf-8") as f:
                json.dump(self.reminders, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения: {e}")
    
    def add_reminder(self, title, message, delay_minutes=1):
        """Добавить напоминание"""
        reminder = {
            "id": int(time.time() * 1000),
            "title": title,
            "message": message,
            "timestamp": time.time() + (delay_minutes * 60),
            "created": time.time()
        }
        
        self.reminders.append(reminder)
        self.save_reminders()
        return reminder["id"]
    
    def start_checker(self):
        """Запуск проверки напоминаний"""
        def check_reminders():
            while True:
                current_time = time.time()
                for reminder in self.reminders[:]:
                    if reminder["timestamp"] <= current_time:
                        # Показываем уведомление
                        self.notification_manager.show_notification(
                            reminder["title"],
                            reminder["message"]
                        )
                        # Удаляем выполненное напоминание
                        self.reminders.remove(reminder)
                        self.save_reminders()
                
                time.sleep(10)
        
        import threading
        thread = threading.Thread(target=check_reminders, daemon=True)
        thread.start()

def main(page: ft.Page):
    page.title = "Голосовые заметки"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    
    # Инициализация менеджеров
    notification = NativeNotification(page)
    recorder = VoiceRecorder(page)
    reminders = ReminderManager(notification)
    
    # Создаем канал уведомлений при запуске
    notification.show_notification("Голосовые заметки", "Приложение запущено")
    
    # Элементы интерфейса
    status_text = ft.Text("Готов к работе", size=18, color=ft.colors.GREEN)
    
    def start_recording(e):
        if recorder.start_recording():
            status_text.value = "🎤 Идет запись..."
            status_text.color = ft.colors.RED
            start_btn.disabled = True
            stop_btn.disabled = False
            page.update()
    
    def stop_recording(e):
        if recorder.stop_recording():
            status_text.value = "✅ Запись завершена"
            status_text.color = ft.colors.GREEN
            start_btn.disabled = False
            stop_btn.disabled = True
            
            notification.show_notification(
                "Голосовая заметка",
                "Запись успешно сохранена"
            )
            page.update()
    
    def test_notification(e):
        notification.show_notification("Тест", "Уведомление работает!")
        status_text.value = "📢 Тестовое уведомление отправлено"
        page.update()
    
    def add_reminder(e):
        reminder_id = reminders.add_reminder(
            "Напоминание",
            "Проверить голосовые записи",
            delay_minutes=2
        )
        status_text.value = f"⏰ Напоминание #{reminder_id} установлено"
        page.update()
    
    # Кнопки интерфейса
    start_btn = ft.ElevatedButton(
        "🎤 Начать запись",
        on_click=start_recording,
        icon=ft.icons.MIC
    )
    
    stop_btn = ft.ElevatedButton(
        "⏹️ Остановить",
        on_click=stop_recording,
        disabled=True,
        icon=ft.icons.STOP
    )
    
    test_btn = ft.ElevatedButton(
        "📢 Тест уведомления",
        on_click=test_notification
    )
    
    reminder_btn = ft.ElevatedButton(
        "⏰ Напомнить через 2 мин",
        on_click=add_reminder
    )
    
    # Компоновка
    page.add(
        ft.Column([
            ft.Text("Голосовые заметки", size=24, weight=ft.FontWeight.BOLD),
            status_text,
            ft.Row([start_btn, stop_btn]),
            ft.Row([test_btn, reminder_btn]),
        ])
    )

if __name__ == "__main__":
    ft.app(target=main)
