import sentry_sdk
import time

sentry_sdk.init(
    dsn="https://e07e9dc6b642df391abefa559827f089@o4511597950533632.ingest.de.sentry.io/4511597986512976",
    traces_sample_rate=1.0,
    shutdown_timeout=10,
)

# Событие 1: деление на ноль
try:
    1 / 0
except ZeroDivisionError as e:
    sentry_sdk.capture_exception(e)

# Событие 2: кастомное сообщение с уровнем warning
sentry_sdk.capture_message("Тестовое предупреждение: высокая нагрузка CPU", level="warning")

# Событие 3: кастомное сообщение с дополнительными данными
with sentry_sdk.configure_scope() as scope:
    scope.set_extra("username", "test_user")
    scope.set_extra("action", "button_click")
    sentry_sdk.capture_message("Пользователь нажал кнопку 'Отправить'", level="info")

# Событие 4: ошибка с контекстом
try:
    items = []
    print(items[0])  # IndexError
except IndexError as e:
    sentry_sdk.capture_exception(e)

print("Все события отправлены!")
time.sleep(5)