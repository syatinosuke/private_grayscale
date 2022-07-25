from distutils.command.clean import clean
from distutils.log import error
from multiprocessing import context
import os
from turtle import title
from wsgiref import validate
from django import forms
from django.core.mail import EmailMessage

from.validate import validate_admin
from.models import Grayscale

class InquiryForm(forms.Form):
    name = forms.CharField(label='お名前', max_length=30)
    email = forms.EmailField(label='メールアドレス', validators=[validate_admin])
    title = forms.CharField(label='タイトル', max_length=30)
    def clean_title(self):
        title = self.cleaned_data['title']
        if title in ['hoge', '阿呆', 'fuck']:
            raise forms.ValidationError('この言葉は使えません')
        return title
    message = forms.CharField(label='メッセージ', widget=forms.Textarea)

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        message = cleaned_data.get('message')

        if title == message:
            raise forms.ValidationError('タイトルと同じものは使えません')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['placeholder'] = 'お名前をここに入力してください。'

        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'メールアドレスをここに入力してください。'

        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['title'].widget.attrs['placeholder'] = 'タイトルをここに入力してください。'

        self.fields['message'].widget.attrs['class'] = 'form-control'
        self.fields['message'].widget.attrs['placeholder'] = 'メッセージをここに入力してください。'

    def send_email(self):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        title = self.cleaned_data['title']
        message = self.cleaned_data['message']

        subject = 'お問い合わせ {}'.format(title)
        message = '送信者名: {0}\nメールアドレス: {1}\nメッセージ:\n{2}'.format(name, email, message)
        from_email = os.environ.get('FROM_EMAIL')
        to_list = [
            os.environ.get('FROM_EMAIL')
        ]
        cc_list = [
            email
        ]

        message = EmailMessage(subject=subject, body=message, from_email=from_email, to=to_list, cc=cc_list)
        message.send()

class GrayscaleCreateForm(forms.ModelForm):
    class Meta:
        model = Grayscale
        fields = ('title', 'content', 'photo1', 'photo2', 'photo3', )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

