from django.shortcuts import render, redirect
from .models import Movie, Comment
from .forms import MovieForm, CommentForm
from django.views.decorators.http import require_POST, require_safe


def index(request):
    movies = Movie.objects.all()
    context = {
        'movies': movies,
    }
    return render(request, 'movies/index.html', context)


def create(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.user_id = request.user
            movie.save()
            return redirect('movies:detail', movie.pk)
    else:
        form = MovieForm()
    context = {
        'form': form,
    }
    return render(request, 'movies/create.html', context)


def detail(request, pk):
    movie = Movie.objects.get(pk=pk)
    comment_form = CommentForm()
    comments = movie.comment_set.all()
    context = {
        'comment_form' : comment_form,
        'movie': movie,
        'comments': comments,
    }
    return render(request, 'movies/detail.html', context)


def delete(request, pk):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    movie = Movie.objects.get(pk=pk)
    if request.user == movie.user_id:
        movie.delete()
        return redirect('movies:index')
    return redirect('movies:detial', pk)


def update(request, pk):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    movie = Movie.objects.get(pk=pk)
    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movies:detail', movie.pk)
    else:
        form = MovieForm(instance=movie)
    context = {
        'movie': movie,
        'form': form,
    }
    return render(request, 'movies/update.html', context)

def comments_create(request, movie_pk):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    comment_form = CommentForm(request.POST)    
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.movie_id = Movie.objects.get(pk=movie_pk)
        comment.user_id = request.user
        comment.save()
        return redirect('movies:detail', pk=movie_pk)
    
@require_POST
def comments_delete(request, movie_pk, comment_pk):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    comments =Comment.objects.get(pk=comment_pk)
    comments.delete()
    return redirect('movies:detail', pk = movie_pk)

@require_POST
def likes(request, pk):
    if request.user.is_authenticated:
        movie = Movie.objects.get(pk=pk)
        if movie.like_users.filter(pk=request.user.pk).exists():
            movie.like_users.remove(request.user)
        else:
            movie.like_users.add(request.user)
        return redirect('movies:index')
    return redirect('accounts:login')