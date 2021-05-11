from django.forms import ModelForm
from .models import Comentario
import requests
from django.conf import settings


class FormComentario(ModelForm):

    def clean(self):
        url = "https://www.google.com/recaptcha/api/siteverify"
        raw_data = self.data

        print(raw_data)

        captcha_rs = raw_data.get('g-recaptcha-response')

        params = {
            'secret': settings.RECAPTCHA_SECRET_KEY,
            'response': captcha_rs,
        }

        verify_rs = requests.get(url, params=params, verify=True)
        verify_rs = verify_rs.json()

        if not verify_rs.get("success", False):
            self.add_error(
                'comentario',
                'Revalide o captcha'
            )

        # response["status"] = verify_rs.get("success", False)
        # response['message'] = verify_rs.get(
        #     'error-codes', None) or "Unspecified error."
        # return HttpResponse(response)

        data = self.cleaned_data
        nome = data.get('nome_comentario')
        email = data.get('email_comentario')
        comentario = data.get('comentario')

        if len(nome) < 5:
            self.add_error(
                'nome_comentario',
                'Deve ter mais que 5 caracteres!'
            )

    class Meta:
        model = Comentario
        fields = ('nome_comentario', 'email_comentario', 'comentario')
