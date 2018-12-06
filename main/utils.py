import requests
from django.conf import settings
import subprocess
from crontab import CronTab

# Добавить запись в iptables
def add_iptables_rule(ip, port):
    try:
        subprocess.call('iptables -A INPUT -p tcp -s {} --dport {} -j ACCEPT'.format(ip, port))
    except:
        pass

# Установить задачу в кронтаб
def add_cron_job(ip, port):
    # TO DO
    pass

# Получить IP из запроса
def get_client_ip(request):
    try:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    except:
        return ""


# Отправить сообщение в телеграм
def telegram_send_message(message, chat_id=settings.TELEGRAM_BOT_SETTINGS['CHAT_ID']):
    url = settings.TELEGRAM_BOT_SETTINGS['API_URL'] + '/sendMessage'
    params = {
        'chat_id': chat_id,
        'text': message
    }
    return requests.post(url, params)
