
# URL configuration for backend project.
# urls.py

from django.urls import path
from django.views import *

from HumanEvaluationFramework.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('init/', init, name='init'),
    path('login/', login, name='login'),
    path('list_datasets/', list_datasets, name='list_datasets'),
    path('start_new_session/', start_new_session, name='start_new_session'),
    path('load_previous_session/', load_previous_session, name='load_previous_session'),
    path('enter_choice/', enter_choice, name='enter_choice'),
    path('finalize/', finalize, name='finalize'),
    path('results/', results, name='results'),
    path('', vue_app, name='vue_app'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
