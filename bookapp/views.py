from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import fetch_books
# import json
from django.http import JsonResponse
from .models import Recommendation, User, Comment
from django.db.models import Q
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
        user.save()
        return redirect('login')
    return render(request, 'registration.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('book_recommendation')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

def book_recommendation(request):
    username = request.user.username if request.user.is_authenticated else None
    return render(request, 'home.html', {'username': username})

def add_comment(request, recommendation_id):
    if request.method == 'POST':
        text = request.POST.get('text')
        recommendation = Recommendation.objects.get(pk=recommendation_id)
        comment = Comment.objects.create(recommendation=recommendation, user=request.user, text=text)
        return redirect('recommended_books')
    
def like_recommendation(request):
    if request.method == 'POST':
        recommendation_id = request.POST.get('recommendation_id')
        recommendation = Recommendation.objects.get(pk=recommendation_id)
        recommendation.likes += 1
        recommendation.save()
        return JsonResponse({'likes': recommendation.likes})
    return JsonResponse({'error': 'Invalid request'})

@api_view(['GET'])
def search_books(request):
    query = request.query_params.get('q', '')
    if query:
        data = fetch_books(query)
        #writing a creating a text file to check the response for debugging purpose
        # with open('google_books_data.txt', 'w') as file:
        #     file.write(json.dumps(data, indent=4)) 
        if data and 'items' in data:
            books = []
            for item in data['items']:
                book_info = item['volumeInfo']
                book_access = item['accessInfo']
                book = {
                    'title': book_info.get('title'),
                    'authors': book_info.get('authors'),
                    'link': book_access.get('webReaderLink', '#'),
                    'category': book_info.get('categories', []),
                    'description': book_info.get('description'),
                    'cover_image': book_info.get('imageLinks', {}).get('thumbnail'),
                    'ratings_count': book_info.get('ratingsCount'),
                    'average_rating': book_info.get('averageRating'),
                    'publication_date': book_info.get('publishedDate')
                }
                books.append(book)
            return Response(books)
        return Response({'error': 'No books found for this query'}, status=404)
    return Response({'error': 'No query provided'}, status=400)

@api_view(['POST'])
def add_to_recommendations(request):
    if request.method == 'POST':
        book_data = {
            'book_title': request.POST.get('book_title'),
            'book_description': request.POST.get('book_description'),
            'author': request.POST.get('author'),
            'link': request.POST.get('link'),
            'cover_image': request.POST.get('cover_image'),
            'rating': request.POST.get('rating'),
            'category': request.POST.get('category'),
            'publication_date': request.POST.get('publication_date'),
        }
        user = request.user
        recommendation = Recommendation(user=user, **book_data)
        recommendation.save()
        return JsonResponse({'message': 'Book added to recommendations successfully'})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

def view_recommendations(request):
    if request.user.is_authenticated:
        recommendations = Recommendation.objects.filter(user=request.user)
        print(recommendations)
        return render(request, 'my_recommendations.html', {'recommendations': recommendations})
    else:
        return redirect('login')
    

def recommended_books(request):
    recommendations = Recommendation.objects.all()
    genres = Recommendation.objects.values_list('category', flat=True).distinct()
    category = request.GET.get('category')
    if category:
        recommendations = recommendations.filter(category=category)
    sort_by = request.GET.get('sort_by')
    if sort_by == 'rating':
        recommendations = recommendations.order_by('-rating')
    elif sort_by == 'publication_date':
        recommendations = recommendations.order_by('-publication_date')
    recommendation_count = recommendations.count()
    context = {
        'recommendations': recommendations,
        'genres': genres,
        'recommendation_count': recommendation_count
    }
    return render(request, 'recommended_books.html', context)

@login_required
def recommend_book_form(request):
    if request.method == 'POST':
        book_title = request.POST.get('book_title')
        author = request.POST.get('author')
        category = request.POST.get('category')
        link = request.POST.get('link')
        book_description = request.POST.get('book_description')
        publication_date = request.POST.get('publication_date')
        recommendation = Recommendation.objects.create(
            user=request.user,
            book_title=book_title,
            author=author,
            category=category,
            link=link,
            book_description=book_description,
            publication_date=publication_date,
        )
        # return JsonResponse({'success': True, 'message': 'Book recommended successfully', 'redirect_url': 'recommended_books'})
        return redirect('recommended_books')

    return render(request, 'recommend_book_form.html')