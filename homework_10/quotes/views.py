from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.db.utils import OperationalError, IntegrityError

from .connect_mongo import authors_from_mongodb, quotes_from_mongodb
from .forms import TagForm, QuoteForm, AuthorForm, QuoteAddTag
from .models import Tag, Quote, Author



def main(request):
    quotes = Quote.objects.filter().all()
    return render(request, 'quotes/index.html', {"quotes": quotes})

class UpdateQuote(UpdateView):
    model = Quote
    fields = ["description"]
    template_name_suffix = "_update_form"
    success_url = reverse_lazy('quotes:main')

def quote_add_tag(request, quote_id):
    quote = get_object_or_404(Quote, pk=quote_id)
    tags = Tag.objects.all()
    if request.method == 'POST':
        form = QuoteAddTag(request.POST)
        if form.is_valid():
            new_tag = form.cleaned_data['new_tag'][0]
            print(new_tag,type(new_tag))
            quote.tags.add(new_tag)
            return redirect(to='quotes:main')
    else:
        form = QuoteAddTag()
    return render(request, 'quotes/quote_add_tag.html', {'form': form, 'tags': tags, 'quotes': quote})

def tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.user = request.user
            tag.save()
            return redirect(to='quotes:main')
        else:
            return render(request, 'quotes/tag.html', {'form': form})

    return render(request, 'quotes/tag.html', {'form': TagForm()})

def search_by_tag(request, tag_name):
    quotes = Quote.objects.filter(tags__name=tag_name).all()
    return render(request, 'quotes/search_by_tag.html', {'quotes': quotes})

def detail(request, quote_id):
    quotes = get_object_or_404(Quote, pk=quote_id)
    authors = Author.objects.all()
    return render(request, 'quotes/detail.html', {"quotes": quotes, "authors": authors})


@login_required
def set_done(request, quote_id):
    Quote.objects.filter(pk=quote_id, user=request.user).update(done=True)
    return redirect(to='quotes:main')

@login_required
def quote_hide(request, quote_id):
    Quote.objects.filter(pk=quote_id, user=request.user).update(done=False)
    return redirect(to='quotes:main')

@login_required
def delete_quote(request, quote_id):
    Quote.objects.get(pk=quote_id, user=request.user).delete()
    return redirect(to='quotes:main')

def author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            new_author = form.save(commit=False)
            new_author.user = request.user
            new_author.save()

            return redirect(to='quotes:main')
        else:
            return render(request, 'quotes/author.html', {'form': form})

    return render(request, 'quotes/author.html', {'form': AuthorForm()})

def quote(request):
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


            return redirect(to='quotes:main')
        else:
            return render(request, 'quotes/quote.html', {"tags": tags, "authors": authors, 'form': form})

    return render(request, 'quotes/quote.html', {"tags": tags, "authors": authors, 'form': QuoteForm()})

def author_datail(request, author_id):

    author = get_object_or_404(Author, pk = author_id)
    return render(request, "quotes/author_detail.html", {"author": author})


def authors_seeds_from_mongodb(*args,**kwargs):
    data = authors_from_mongodb()
    for item in data:
        _description = item.get('description')
        if len(_description) > 2704:
            _description = _description[0:2704]
        try:
            Author.objects.create(full_name= item.get('full_name'),
                  born_date= item.get('born_date'),
                  born_location= item.get('born_location'),
                  description= _description)
        except (OperationalError, IntegrityError) as err:     
            print(err)
            continue


def quotes_seeds_from_mongodb(request):
    data = quotes_from_mongodb()
    for item in data:
        quote = str
        tags = []
        author = Author
        quote = item.get('quote')
        for tag in item.get('tags'):
            tags.append(Tag.objects.filter(name= tag.get('name'),user=request.user).first())
        author = Author.objects.filter(full_name= item.get('author'),user=request.user).first()
        result = Quote.objects.create(description=quote, done=True)
        result.save()
        result.author.add(author)
        for tag in tags:
            result.tags.add(tag)

        
def tags_seeds_from_mongodb(*args, **kwargs):
    data = quotes_from_mongodb()

    for item in data:
        for tag in item.get('tags'):
            try:
                Tag.objects.create(name= tag.get('name'))
            except IntegrityError as er:
                print(er)
                continue


def migrate_from_mongo_to_postger(request, *args, **kwargs):
    authors_seeds_from_mongodb(request)
    tags_seeds_from_mongodb(request)
    quotes_seeds_from_mongodb(request)
    return redirect(to="quotes:main")




