from django.contrib import admin
from django.urls import path, include
from todolist import views as todolist_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', todolist_view.index, name='index'),
    path('todolist/', include('todolist.urls')),
    path('account/', include('users_app.urls')),
    path('contact', todolist_view.contact, name='contact'),
    path('about', todolist_view.about, name='about')
]
