from django.urls import path
from . import views

app_name = 'quotes'

urlpatterns = [
    path('', views.main, name='main'),
    path('index/', views.main, name='index'),
    path('author/', views.author, name='author'),
    path('author_detail/<int:author_id>', views.author_datail, name='author_detail'),
    path('tag/', views.tag, name='tag'),
    path('quote/', views.quote, name='quote'),
    path("quote/<int:pk>/update", views.UpdateQuote.as_view(), name="quote_update"),
    path("quote/quote_add_tag/<int:quote_id>", views.quote_add_tag, name="quote_add_tag"),
    path('detail/<int:quote_id>', views.detail, name='detail'),
    path('quote_hide/<int:quote_id>', views.quote_hide, name='quote_hide'),
    path('done/<int:quote_id>', views.set_done, name='set_done'),
    path('delete/<int:quote_id>', views.delete_quote, name='delete'),
    path('search_by_tag/<str:tag_name>/', views.search_by_tag, name='search_by_tag'),
]

