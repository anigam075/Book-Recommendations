from django.urls import path
from .views import *

urlpatterns = [
    path('', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('book_recommendation/', book_recommendation, name='book_recommendation'),
    path('search/', search_books, name='search_books'),
    path('add-to-recommendations/', add_to_recommendations, name='add_to_recommendations'),
    path('recommendations/', view_recommendations, name='view_recommendations'),
    path('recommended-books/', recommended_books, name='recommended_books'), 
    path('add-comment/<int:recommendation_id>/', add_comment, name='add_comment'),
    path('like_recommendation/', like_recommendation, name='like_recommendation'),
    path('recommend_book_form/', recommend_book_form, name='recommend_book_form'),
]
