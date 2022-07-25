from asyncio.log import logger
from multiprocessing import context
#from typing_extensions import Self
from django.shortcuts import render

# Create your views here.
import logging
from django.urls import reverse_lazy

from django.views import generic
from.forms import InquiryForm

from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin
from.models import Grayscale

from.forms import InquiryForm,GrayscaleCreateForm

from django.views.generic import ListView
from django.db.models import Q


from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404


class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        # URLに埋め込まれた主キーから日記データを1件取得。取得できなかった場合は404エラー
        diary = get_object_or_404(Grayscale, pk=self.kwargs['pk'])
        # ログインユーザーと日記の作成ユーザーを比較し、異なればraise_exceptionの設定に従う
        return self.request.user == diary.user

logger = logging.getLogger(__name__)

class IndexView(generic.TemplateView):
    template_name = "index.html"

class InquiryView(generic.FormView):
    template_name = "inquiry.html"
    form_class = InquiryForm

    def get_form(self, form_class=None):
        # contact.hmltで、データを送信した場合
        if 'name' in self.request.POST:
            form_data = self.request.POST
  
        # お問い合わせフォーム確認画面から「戻る」リンクを押した場合や
        # 初回の入力欄表示は以下の表示。
        # セッションにユーザーデータがあれば、それをフォームに束縛
        else:
            form_data = self.request.session.get('form_data', None)
  
        return self.form_class(form_data)

    def form_valid(self, form):
        return render(self.request,'contact_confirm.html',{'form':form})



class contact_confirm(generic.TemplateView):
    """お問い合わせフォーム確認ページ"""
 
    template_name = 'contact_confirm.html'
  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_data = self.request.session.get('form_data', None)
        context['form'] = Grayscale(form_data)
        return context


class contact_send(generic.FormView):
    """お問い合わせ送信"""
 
    template_name = 'inquiry.html'
    form_class = InquiryForm
    success_url = reverse_lazy('grayscale:inquiry')

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request,'メッセージを送信しました。')
        logger.info('Inquiry sent by {}'.format(form.cleaned_data['name']))
        return super().form_valid(form)
        
class GrayscaleListView(LoginRequiredMixin, generic.ListView):
    model = Grayscale
    template_name = 'grayscale_list.html'
    paginate_by=2 #1ページで表示する数

    def get_queryset(self):
        queryset = Grayscale.objects.filter(user=self.request.user).order_by('-created_at')
        #return diaries
    #def get_queryset(self):
        #queryset = Grayscale.objects.order_by('-created_date')
        query = self.request.GET.get('query')

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)
            )
        return queryset

class GrayscaleDetailView(LoginRequiredMixin, OnlyYouMixin, generic.DetailView):
    model = Grayscale
    template_name = 'grayscale_detail.html'

class GrayscaleCreateView(LoginRequiredMixin, generic.CreateView):
    model = Grayscale
    template_name = 'grayscale_create.html'
    form_class = GrayscaleCreateForm
    success_url = reverse_lazy('grayscale:grayscale_list')

    def form_valid(self, form):
        diary = form.save(commit=False)
        diary.user = self.request.user
        diary.save()
        messages.success(self.request, '日記を作成しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "日記の作成に失敗しました。")
        return super().form_invalid(form)

class GrayscaleUpdateView(LoginRequiredMixin, OnlyYouMixin, generic.UpdateView):
    model = Grayscale
    template_name = 'grayscale_update.html'
    form_class = GrayscaleCreateForm

    def get_success_url(self):
        return reverse_lazy('grayscale:grayscale_detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        messages.success(self.request, '日記を更新しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "日記の更新に失敗しました。")
        return super().form_invalid(form)

class GrayscaleDeleteView(LoginRequiredMixin, OnlyYouMixin, generic.DeleteView):
    model = Grayscale
    template_name = 'grayscale_delete.html'
    success_url = reverse_lazy('grayscale:grayscale_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "日記を削除しました。")
        return super().delete(request, *args, **kwargs)

    