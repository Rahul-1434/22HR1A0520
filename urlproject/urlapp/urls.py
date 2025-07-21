from django.urls import path
from .views import ShortURLCreateView, ShortURLStatsView, redirect_view

urlpatterns = [
    path('shorturls/', ShortURLCreateView.as_view(), name='create_shorturl'),
    path('shorturls/<str:shortcode>/', ShortURLStatsView.as_view(), name='stats_shorturl'),
    path('r/<str:shortcode>/', redirect_view, name='redirect_shorturl'),
]

