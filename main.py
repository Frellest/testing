import flet as ft

class SimpleNotification:
    def __init__(self):
        self.can_notify = False
        self._init_notifications()
    
    def _init_notifications(self):
        """Простая инициализация без сложной логики"""
        try:
            from jnius import autoclass
            
            # Только базовые импорты
            self.PythonActivity = autoclass('org.kivy.android.PythonActivity')
            self.Context = autoclass('android.content.Context')
            
            self.context = self.PythonActivity.mActivity
            self.can_notify = True
            return "✅ Android API available"
            
        except Exception as e:
            return f"❌ Android API: {str(e)}"
    
    def send_simple_notification(self, title, message):
        """Упрощенная отправка уведомлений"""
        if not self.can_notify:
            return False
            
        try:
            from jnius import autoclass
            
            NotificationManager = autoclass('android.app.NotificationManager')
            NotificationBuilder = autoclass('android.app.Notification$Builder')
            
            # Простое уведомление без каналов (для старых API)
            builder = NotificationBuilder(self.context)
            builder.setContentTitle(title)
            builder.setContentText(message)
            builder.setSmallIcon(android.R.drawable.ic_dialog_info)
            
            notification_manager = self.context.getSystemService(self.Context.NOTIFICATION_SERVICE)
            notification_manager.notify(1, builder.build())
            return True
            
        except Exception as e:
            print(f"Notification error: {e}")
            return False

def main(page: ft.Page):
    page.title = "Simple Notifications"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.colors.WHITE
    
    notifier = SimpleNotification()
    init_status = notifier._init_notifications()
    
    status_text = ft.Text(init_status, size=14)
    result_text = ft.Text("Press button to test", size=16)
    
    def send_test(e):
        success = notifier.send_simple_notification(
            "Test Title", 
            "Test Message"
        )
        if success:
            result_text.value = "✅ Notification sent!"
            result_text.color = ft.colors.GREEN
        else:
            result_text.value = "❌ Failed to send notification"
            result_text.color = ft.colors.RED
        page.update()
    
    page.add(
        ft.Column([
            ft.Text("Simple Notification Test", size=24),
            status_text,
            ft.ElevatedButton("Send Test Notification", on_click=send_test),
            result_text,
        ])
    )

ft.app(target=main)
