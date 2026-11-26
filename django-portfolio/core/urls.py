from django.urls import include, path

urlpatterns = [
    path('', include('portfolio_app.urls')),
]
