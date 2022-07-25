from django.urls import path

from . import views


app_name = 'grayscale'
urlpatterns = [
    path("",views.IndexView.as_view(), name="index"),
    path('inquiry/', views.InquiryView.as_view(), name="inquiry"),
    path('contact-confirm/', views.contact_confirm.as_view(), name="contact_confirm"),
    path('contact-send/', views.contact_send.as_view(), name="contact_send"),
    path('grayscale-list/', views.GrayscaleListView.as_view(), name="grayscale_list"),
    path('grayscale-detail/<int:pk>/', views.GrayscaleDetailView.as_view(), name="grayscale_detail"),
    path('grayscale-create/', views.GrayscaleCreateView.as_view(), name="grayscale_create"),
    path('grayscale-update/<int:pk>/', views.GrayscaleUpdateView.as_view(), name="grayscale_update"),
    path('grayscale-delete/<int:pk>/', views.GrayscaleDeleteView.as_view(), name="grayscale_delete"),

]
