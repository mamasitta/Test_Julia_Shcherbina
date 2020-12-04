from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name="login"),
    # path('', views.some_view ),
    path('', views.index, name='index'),
    path('create_schema', views.create_schema, name="create_schema"),
    path('logout', views.logout_view, name="logout"),
    path('schema_delete/<int:schema_id>', views.schema_delete, name='schema_delete'),
    path('data_sets', views.data_sets, name="data_sets"),
]
