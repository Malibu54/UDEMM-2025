from abc import ABC, abstractmethod

class Notification(ABC):
    @abstractmethod
    def send(self, message: str) -> None:
        pass


class EmailNotification(Notification):
    def __init__(self, recipient: str):
        self.recipient = recipient

    def send(self, message: str) -> None:
        print(f"[EMAIL] Para: {self.recipient} | {message}")


class SMSNotification(Notification):
    def __init__(self, phone: str):
        self.phone = phone

    def send(self, message: str) -> None:
        print(f"[SMS] Teléfono: {self.phone} | {message}")


class AppNotification(Notification):
    def __init__(self, user_token: str):
        self.user_token = user_token

    def send(self, message: str) -> None:
        print(f"[APP] Token: {self.user_token} | {message}")


class Notifier(ABC):
    @abstractmethod
    def create_notification(self) -> Notification:
        pass

    def notify(self, message: str) -> None:
        notification = self.create_notification()
        notification.send(message)


class EmailNotifier(Notifier):
    def __init__(self, recipient: str):
        self.recipient = recipient

    def create_notification(self) -> Notification:
        return EmailNotification(self.recipient)


class SMSNotifier(Notifier):
    def __init__(self, phone: str):
        self.phone = phone

    def create_notification(self) -> Notification:
        return SMSNotification(self.phone)


class AppNotifier(Notifier):
    def __init__(self, user_token: str):
        self.user_token = user_token

    def create_notification(self) -> Notification:
        return AppNotification(self.user_token)


if __name__ == "__main__":
    notifiers: list[Notifier] = [
        EmailNotifier("ops@empresa.com"),
        SMSNotifier("+541199887766"),
        AppNotifier("device-token-abc-123"),
    ]

    for notifier in notifiers:
        notifier.notify("ALERTA: CPU > 90% en prod-server-01")