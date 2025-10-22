import flet as ft
import os

class NotificationApp:
    def __init__(self):
        self.notification_manager = self._init_notification_manager()
    
    def _init_notification_manager(self):
        """Инициализация менеджера уведомлений"""
        try:
            # Пытаемся использовать Pyjnius
            from jnius import autoclass
            print("✅ Pyjnius доступен")
            return AndroidNotification()
        except Exception as e:
            print(f"❌ Pyjnius недоступен: {e}")
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
        self.initialized = self._init_android()
    
    def _init_android(self):
        """Инициализация Android компонентов"""
        try:
            from jnius import autoclass, cast
            
            # Импортируем Android классы
            self.PythonActivity = autoclass('org.kivy.android.PythonActivity')
            self.Context = autoclass('android.content.Context')
            self.NotificationManager = autoclass('android.app.NotificationManager')
            self.NotificationCompat = autoclass('androidx.core.app.NotificationCompat')
            self.NotificationChannel = autoclass('android.app.NotificationChannel')
            self.NotificationBuilder = autoclass('android.app.Notification$Builder')
            self.Intent = autoclass('android.content.Intent')
            self.PendingIntent = autoclass('android.app.PendingIntent')
            
            # Получаем контекст
            self.context = self.PythonActivity.mActivity
            
            # Создаем канал уведомлений
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
            
            # Получаем NotificationManager
            notification_service = self.context.getSystemService(self.Context.NOTIFICATION_SERVICE)
            self.notification_manager = self.NotificationManager.cast(notification_service)
            
            # Создаем канал (для API 26+)
            importance = self.NotificationManager.IMPORTANCE_HIGH
            channel = self.NotificationChannel(channel_id, channel_name, importance)
            channel.setDescription("Уведомления от Flet приложения")
            self.notification_manager.createNotificationChannel(channel)
            
            self.channel_id = channel_id
            print("✅ Канал уведомлений создан")
            
        except Exception as e:
            print(f"❌ Ошибка создания канала: {e}")
    
    def send_notification(self, title, message):
        """Отправить уведомление"""
        try:
            # Intent для открытия приложения
            intent = self.Intent(self.context, self.PythonActivity)
            intent.setFlags(self.Intent.FLAG_ACTIVITY_NEW_TASK | self.Intent.FLAG_ACTIVITY_CLEAR_TASK)
            
            pending_intent = self.PendingIntent.getActivity(
                self.context, 0, intent, 
                self.PendingIntent.FLAG_UPDATE_CURRENT | self.PendingIntent.FLAG_IMMUTABLE
            )
            
            # Создаем уведомление через NotificationCompat для совместимости
            builder = self.NotificationCompat.Builder(self.context, self.channel_id)
            builder.setContentTitle(title)
            builder.setContentText(message)
            builder.setSmallIcon(android.R.drawable.ic_dialog_info)
            builder.setContentIntent(pending_intent)
            builder.setAutoCancel(True)
            builder.setPriority(self.NotificationCompat.PRIORITY_HIGH)
            
            # Показываем уведомление
            notification = builder.build()
            self.notification_manager.notify(1, notification)
            
            print("✅ Уведомление отправлено через Pyjnius")
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
    page.padding = 20
    
    # Проверяем доступность Pyjnius
    try:
        from jnius import autoclass
        pyjnius_status = "✅ Pyjnius доступен"
        status_color = ft.colors.GREEN
    except Exception as e:
        pyjnius_status = f"❌ Pyjnius недоступен: {e}"
        status_color = ft.colors.RED
    
    app = NotificationApp()
    
    result_text = ft.Text("Нажмите кнопку для теста", size=16)
    counter_text = ft.Text("Отправлено: 0", size=14, color=ft.colors.GREY_400)
    status_text = ft.Text(pyjnius_status, size=12, color=status_color)
    counter = 0
    
    def button_clicked(e):
        nonlocal counter
        success = app.send_test_notification()
        
        if success:
            counter += 1
            result_text.value = "✅ Уведомление отправлено!"
            result_text.color = ft.colors.GREEN
            counter_text.value = f"Отправлено: {counter}"
            
            # Показываем snackbar
            page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text("Уведомление отправлено через Pyjnius!"),
                    action="OK"
                )
            )
        else:
            result_text.value = "❌ Ошибка отправки уведомления"
            result_text.color = ft.colors.RED
        
        page.update()
    
    page.add(
        ft.Column([
            ft.Icon(ft.icons.NOTIFICATIONS_ACTIVE, size=80, color=ft.colors.BLUE_400),
            ft.Text("Тест Pyjnius уведомлений", 
                   size=28, 
                   weight=ft.FontWeight.BOLD,
                   text_align=ft.TextAlign.CENTER),
            ft.Text("Flet 0.28.3 + Flutter 3.29.2", 
                   size=16,
                   color=ft.colors.BLUE_200,
                   text_align=ft.TextAlign.CENTER),
            
            ft.Container(height=30),
            
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        status_text,
                        ft.Divider(height=10),
                        result_text,
                        counter_text,
                    ]),
                    padding=20,
                ),
                elevation=5
            ),
            
            ft.Container(height=20),
            
            ft.FilledButton(
                content=ft.Row([
                    ft.Icon(ft.icons.SEND_AND_ARCHIVE),
                    ft.Text("Отправить тестовое уведомление", size=16),
                ], alignment=ft.MainAxisAlignment.CENTER),
                on_click=button_clicked,
                style=ft.ButtonStyle(
                    padding=ft.padding.symmetric(horizontal=30, vertical=15),
                    shape=ft.RoundedRectangleBorder(radius=10)
                )
            ),
            
            ft.Container(height=30),
            
            ft.Text(
                "Приложение использует Pyjnius для нативных Android уведомлений\n"
                "Версия: Flet 0.28.3 + Flutter 3.29.2",
                size=12,
                color=ft.colors.GREY_500,
                text_align=ft.TextAlign.CENTER
            )
        ], 
        alignment=ft.MainAxisAlignment.CENTER, 
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10)
    )

if __name__ == "__main__":
    ft.app(target=main)