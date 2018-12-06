from django.shortcuts import render
from django.contrib.auth.views import login_required
from .models import AccessToken
from datetime import datetime, timedelta
import os
import binascii
from .utils import telegram_send_message, get_client_ip, add_iptables_rule
from django.core.exceptions import ObjectDoesNotExist
import pytz


# Create your views here.

@login_required
def allow_ip(request):
    if request.method == 'GET':
        return render(request, 'allow_ip.html')
    elif request.method == 'POST':
        # Генерируем код подтверждения
        access_token = binascii.hexlify(os.urandom(5)).decode()
        try:
            token_object = AccessToken.objects.get(user=request.user)
        except ObjectDoesNotExist:
            token_object = AccessToken(user=request.user)
        token_object.access_token = access_token
        token_object.token_expiration_datetime = datetime.now() + timedelta(hours=1)
        token_object.save()

        # Отправляем код в телеграм
        telegram_send_message(access_token)

        return render(request, 'validate_token.html')


@login_required
def validate_token(request):
    if request.method == 'POST':
        data = request.POST.copy()
        token = data.get('access_token')
        try:
            token_obj = AccessToken.objects.get(access_token=token)
            if token_obj.token_expiration_datetime < pytz.utc.localize(datetime.now()):
                is_valid = False
            else:
                is_valid = True

                # Открываем доступ по этому айпишнику
                ip = get_client_ip(request)
                port = 22
                add_iptables_rule(ip, port)

        except ObjectDoesNotExist:
            is_valid = False

        return render(request, 'final.html', context={'is_valid': is_valid})
