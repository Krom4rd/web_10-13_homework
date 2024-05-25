from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy, reverse

from .forms import TagForm, QuoteForm, AuthorForm
from .models import Tag, Quote, Author

def index(request):
    quotes = Quote.objects.filter().all()
    return render(request, 'quotes/index.html', {"quotes": quotes})

class UpdateQuote(UpdateView):
    model = Quote
    fields = ["description"]
    template_name_suffix = "_update_form"
    success_url = reverse_lazy('quotes:index')

def tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.user = request.user
            tag.save()
            return redirect(to='quotes:index')
        else:
            return render(request, 'quotes/tag.html', {'form': form})

    return render(request, 'quotes/tag.html', {'form': TagForm()})


def detail(request, quote_id):
    quotes = get_object_or_404(Quote, pk=quote_id)
    authors = Author.objects.all()
    return render(request, 'quotes/detail.html', {"quotes": quotes, "authors": authors})


@login_required
def set_done(request, quote_id):
    Quote.objects.filter(pk=quote_id, user=request.user).update(done=True)
    return redirect(to='quotes:index')


@login_required
def delete_quote(request, quote_id):
    Quote.objects.get(pk=quote_id, user=request.user).delete()
    return redirect(to='quotes:index')

def search_by_tag(request, tag_name):
    quotes = Quote.objects.filter(tags__name=tag_name)
    return render(request, 'search_by_tag.html', {'quotes': quotes, 'tag_name': tag_name})

def author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            new_author = form.save(commit=False)
            new_author.user = request.user
            new_author.save()

            return redirect(to='quotes:index')
        else:
            return render(request, 'quotes/author.html', {'form': form})

    return render(request, 'quotes/author.html', {'form': AuthorForm()})


def quote(request):
    # tags = Tag.objects.filter(user=request.user).all()
    tags = Tag.objects.all()
    authors = Author.objects.all()

    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save(commit=False)
            new_quote.user = request.user
            new_quote.save()
            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'), user=request.user)
            choice_author = Author.objects.filter(full_name__in=request.POST.getlist('authors'), user=request.user)
            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)
            for author in choice_author.iterator():
                new_quote.author.add(author)


            return redirect(to='quotes:index')
        else:
            return render(request, 'quotes/quote.html', {"tags": tags, "authors": authors, 'form': form})

    return render(request, 'quotes/quote.html', {"tags": tags, "authors": authors, 'form': QuoteForm()})

def author_datail(request, author_id):

    author = get_object_or_404(Author, pk = author_id)
    return render(request, "quotes/author_detail.html", {"author": author})





