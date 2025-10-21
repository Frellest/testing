import flet as ft
import os

class NotificationApp:
    def __init__(self):
        self.notification_manager = self._init_notification_manager()
    
    def _init_notification_manager(self):
        """Инициализация менеджера уведомлений"""
        # Проверяем, запущены ли в Android среде
        if 'ANDROID_ARGUMENT' in os.environ:
            from android_notification import AndroidNotification
            return AndroidNotification()
        else:
            from dummy_notification import DummyNotification
            return DummyNotification()
    
    def send_test_notification(self):
        """Отправить тестовое уведомление"""
        try:
            success = self.notification_manager.send_notification(
                "Тестовое уведомление",
                "Привет из Flet приложения! 🎉"
            )
            return success
        except Exception as e:
            print(f"Ошибка уведомления: {e}")
            return False

class AndroidNotification:
    """Реальные Android уведомления через Pyjnius"""
    def __init__(self):
        self._init_android()
    
    def _init_android(self):
        """Инициализация Android компонентов"""
        try:
            from jnius import autoclass
            
            self.Context = autoclass('android.content.Context')
            self.PythonActivity = autoclass('org.kivy.android.PythonActivity')
            self.NotificationManager = autoclass('android.app.NotificationManager')
            self.NotificationChannel = autoclass('android.app.NotificationChannel')
            self.NotificationBuilder = autoclass('android.app.Notification$Builder')
            self.Intent = autoclass('android.content.Intent')
            self.PendingIntent = autoclass('android.app.PendingIntent')
            
            self.context = self.PythonActivity.mActivity
            self._setup_notification_channel()
            
            print("✅ Android уведомления инициализированы")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка инициализации Android: {e}")
            return False
    
    def _setup_notification_channel(self):
        """Настройка канала уведомлений"""
        try:
            channel_id = "flet_app_channel"
            channel_name = "Flet App Notifications"
            importance = self.NotificationManager.IMPORTANCE_HIGH
            
            channel = self.NotificationChannel(channel_id, channel_name, importance)
            channel.setDescription("Уведомления от Flet приложения")
            
            notification_manager = self.context.getSystemService(self.Context.NOTIFICATION_SERVICE)
            notification_manager.createNotificationChannel(channel)
            
            self.channel_id = channel_id
            self.notification_manager = notification_manager
            
        except Exception as e:
            print(f"❌ Ошибка канала: {e}")
    
    def send_notification(self, title, message):
        """Отправить уведомление"""
        try:
            # Intent для открытия приложения
            intent = self.Intent(self.context, self.PythonActivity.getClass())
            pending_intent = self.PendingIntent.getActivity(
                self.context, 0, intent, 
                self.PendingIntent.FLAG_UPDATE_CURRENT | self.PendingIntent.FLAG_IMMUTABLE
            )
            
            # Создаем уведомление
            notification = (self.NotificationBuilder(self.context, self.channel_id)
                          .setContentTitle(title)
                          .setContentText(message)
                          .setSmallIcon(android.R.drawable.ic_dialog_info)
                          .setContentIntent(pending_intent)
                          .setAutoCancel(True)
                          .setPriority(self.NotificationBuilder.PRIORITY_HIGH)
                          .build())
            
            # Показываем уведомление
            self.notification_manager.notify(1, notification)
            return True
            
        except Exception as e:
            print(f"❌ Ошибка отправки уведомления: {e}")
            return False

class DummyNotification:
    """Заглушка для тестирования вне Android"""
    def send_notification(self, title, message):
        print(f"🔔 [ЗАГЛУШКА] {title}: {message}")
        return True

def main(page: ft.Page):
    page.title = "Flet Notification Test"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK
    
    app = NotificationApp()
    
    result_text = ft.Text("Нажмите кнопку для теста", size=16)
    counter_text = ft.Text("Отправлено: 0", size=14, color=ft.Colors.GREY_400)
    counter = 0
    
    def button_clicked(e):
        nonlocal counter
        success = app.send_test_notification()
        
        if success:
            counter += 1
            result_text.value = "✅ Уведомление отправлено!"
            result_text.color = ft.colors.GREEN
            counter_text.value = f"Отправлено: {counter}"
        else:
            result_text.value = "❌ Ошибка отправки уведомления"
            result_text.color = ft.colors.RED
        
        page.update()
    
    page.add(
        ft.Column([
            ft.Icon(ft.Icons.NOTIFICATIONS, size=50, color=ft.Colors.BLUE),
            ft.Text("Тест уведомлений", size=24, weight=ft.FontWeight.BOLD),
            ft.Text("Проверка работы Pyjnius в Flet", size=14),
            
            ft.Container(height=20),
            
            ft.ElevatedButton(
                "📨 Отправить уведомление",
                on_click=button_clicked,
                icon=ft.Icons.SEND,
                style=ft.ButtonStyle(
                    color=ft.Colors.WHITE,
                    bgcolor=ft.Colors.BLUE,
                    padding=20
                )
            ),
            
            ft.Container(height=10),
            
            result_text,
            counter_text,
            
            ft.Container(height=20),
            
            ft.Text(
                "Это приложение использует Pyjnius для нативных Android уведомлений",
                size=12,
                color=ft.Colors.GREY_500,
                text_align=ft.TextAlign.CENTER
            )
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

if __name__ == "__main__":
    ft.app(target=main)
