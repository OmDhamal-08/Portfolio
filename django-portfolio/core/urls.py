from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from portfolio_app.sitemaps import SITEMAPS
from portfolio_app.views import robots_txt

urlpatterns = [
    path('sitemap.xml', sitemap, {'sitemaps': SITEMAPS}, name='sitemap'),
    path('robots.txt', robots_txt, name='robots_txt'),
    path('', include('portfolio_app.urls')),
]
