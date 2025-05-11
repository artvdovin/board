from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .models import BaseRegisterForm
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.conf import settings

class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        verification_code = 'Проверочный код'
        verification_url = 'ССылка для регистрации'
        print(user)
        context = {
            'user': user,
            'verification_code': verification_code,
            'verification_url': verification_url,
        }

        # Рендерим HTML и текстовую версии письма
        html_message = render_to_string('sign/verification_email.html', context)
        plain_message = strip_tags(html_message)

        # Отправляем письмо
        send_mail(
            subject='Подтверждение регистрации',
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return response