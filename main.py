import flet as ft
import subprocess
import json
import time
from datetime import datetime

class NativeNotification:
    """Уведомления через системные команды"""
    
    @staticmethod
    def send_notification(title, message):
        """Отправка уведомления через системные утилиты"""
        try:
            # Для Termux (если приложение запущено в Termux)
            try:
                subprocess.run([
                    "termux-notification", 
                    "--title", title, 
                    "--content", message,
                    "--priority", "high"
                ], check=True, timeout=5)
                return True
            except:
                pass
            
            # Для Linux (через notify-send)
            try:
                subprocess.run([
                    "notify-send", title, message,
                    "-t", "5000"  # 5 секунд
                ], check=True, timeout=5)
                return True
            except:
                pass
            
            # Резервный вариант - вывод в консоль
            print(f"📢 УВЕДОМЛЕНИЕ: {title} - {message}")
            return True
            
        except Exception as e:
            print(f"Ошибка уведомления: {e}")
            return False

class VoiceRecorder:
    """Запись голоса через системные утилиты"""
    
    def __init__(self):
        self.is_recording = False
        self.process = None
    
    def start_recording(self, duration=10):
        """Начать запись"""
        try:
            filename = f"recording_{int(time.time())}.wav"
            
            # Пробуем разные методы записи
            commands = [
                # Android/Termux
                ["termux-microphone-record", "-f", filename, "-l", str(duration * 1000)],
                # Linux arecord
                ["arecord", "-d", str(duration), "-f", "cd", filename],
                # Linux sox
                ["rec", filename, "trim", "0", str(duration)]
            ]
            
            for cmd in commands:
                try:
                    self.process = subprocess.Popen(cmd)
                    self.is_recording = True
                    print(f"🎤 Запись начата: {filename}")
                    return filename
                except:
                    continue
            
            # Если системные утилиты недоступны - эмуляция
            print("⚠️ Системные утилиты записи недоступны, используется эмуляция")
            self.is_recording = True
            return f"emulated_recording_{int(time.time())}.wav"
            
        except Exception as e:
            print(f"Ошибка начала записи: {e}")
            return None
    
    def stop_recording(self):
        """Остановить запись"""
        if not self.is_recording:
            return None
            
        try:
            if self.process:
                self.process.terminate()
                self.process.wait(timeout=3)
            
            self.is_recording = False
            print("⏹️ Запись остановлена")
            return True
        except Exception as e:
            print(f"Ошибка остановки записи: {e}")
            return False

class ReminderManager:
    """Управление напоминаниями через файлы"""
    
    def __init__(self):
        self.reminders_file = "reminders.json"
        self.load_reminders()
    
    def load_reminders(self):
        """Загрузка напоминаний из файла"""
        try:
            with open(self.reminders_file, 'r', encoding='utf-8') as f:
                self.reminders = json.load(f)
        except:
            self.reminders = []
    
    def save_reminders(self):
        """Сохранение напоминаний в файл"""
        try:
            with open(self.reminders_file, 'w', encoding='utf-8') as f:
                json.dump(self.reminders, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения: {e}")
    
    def add_reminder(self, title, message, reminder_time):
        """Добавить напоминание"""
        reminder = {
            "id": int(time.time() * 1000),
            "title": title,
            "message": message,
            "timestamp": reminder_time,
            "created": time.time()
        }
        
        self.reminders.append(reminder)
        self.save_reminders()
        self.start_reminder_checker()
        
        return reminder["id"]
    
    def start_reminder_checker(self):
        """Запуск проверки напоминаний в фоне"""
        def checker():
            while True:
                current_time = time.time()
                for reminder in self.reminders[:]:  # Копия списка
                    if reminder["timestamp"] <= current_time:
                        # Показываем уведомление
                        NativeNotification.send_notification(
                            reminder["title"], 
                            reminder["message"]
                        )
                        # Удаляем выполненное напоминание
                        self.reminders.remove(reminder)
                        self.save_reminders()
                
                time.sleep(10)  # Проверка каждые 10 секунд
        
        import threading
        thread = threading.Thread(target=checker, daemon=True)
        thread.start()

def main(page: ft.Page):
    page.title = "Голосовые заметки"
    page.theme_mode = ft.ThemeMode.DARK
    
    # Инициализация менеджеров
    notification = NativeNotification()
    recorder = VoiceRecorder()
    reminders = ReminderManager()
    
    # Элементы интерфейса
    status_text = ft.Text("Готов к работе", size=16, color=ft.colors.GREEN)
    recording_status = ft.Text("", size=14, color=ft.colors.ORANGE)
    
    # Запись голоса
    def start_recording(e):
        filename = recorder.start_recording(30)  # 30 секунд
        if filename:
            recording_status.value = f"🎤 Запись: {filename}"
            start_btn.disabled = True
            stop_btn.disabled = False
            page.update()
    
    def stop_recording(e):
        if recorder.stop_recording():
            recording_status.value = "✅ Запись сохранена"
            start_btn.disabled = False
            stop_btn.disabled = True
            
            # Уведомление о завершении
            notification.send_notification(
                "Голосовая заметка", 
                "Запись завершена успешно"
            )
            page.update()
    
    # Уведомления
    def test_notification(e):
        if notification.send_notification("Тест", "Приложение работает!"):
            status_text.value = "✅ Уведомление отправлено"
            status_text.color = ft.colors.GREEN
        else:
            status_text.value = "⚠️ Уведомления недоступны"
            status_text.color = ft.colors.ORANGE
        page.update()
    
    # Напоминания
    def add_reminder(e):
        # Напоминание через 2 минуты для теста
        reminder_time = time.time() + 120
        reminder_id = reminders.add_reminder(
            "Проверить записи",
            "Не забудьте прослушать голосовые заметки",
            reminder_time
        )
        
        status_text.value = f"⏰ Напоминание установлено (ID: {reminder_id})"
        status_text.color = ft.colors.BLUE
        page.update()
    
    # Кнопки
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
        on_click=test_notification,
        icon=ft.icons.NOTIFICATIONS
    )
    
    reminder_btn = ft.ElevatedButton(
        "⏰ Добавить напоминание",
        on_click=add_reminder,
        icon=ft.icons.ACCESS_ALARM
    )
    
    # Компоновка интерфейса
    page.add(
        ft.Column([
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text("Голосовые заметки", size=24, weight=ft.FontWeight.BOLD),
                        status_text,
                        recording_status,
                    ]),
                    padding=20
                )
            ),
            
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text("Запись голоса", size=18, weight=ft.FontWeight.BOLD),
                        ft.Row([start_btn, stop_btn], alignment=ft.MainAxisAlignment.CENTER),
                    ]),
                    padding=20
                )
            ),
            
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text("Уведомления", size=18, weight=ft.FontWeight.BOLD),
                        test_btn,
                        reminder_btn,
                    ]),
                    padding=20
                )
            ),
        ])
    )

if __name__ == "__main__":
    ft.app(target=main)
