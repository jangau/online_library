import re
from datetime import datetime

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core import serializers
from models import Book, Borrow, Library, Reserve, Review
from forms import ReviewForm, BorrowForm, ReserveForm
from django.db.models import Q


def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:
        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 


def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.
    '''
    query = None  # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None  # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query


def json_serialize(queryset):
    list = eval(serializers.serialize('json', queryset) if len(queryset) else {})
    serialized_list = []
    for item in list:
        item['fields'].update({
            'id': item['pk']
        })
        serialized_list.append(item['fields'])

    return serialized_list


def show_book(request, id_book):
    authenticated = False
    if request.user.is_authenticated():
        authenticated = True

    book = Book.objects.get(id_book=id_book)
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.book = book
            new_review.user = request.user
            new_review.save()

    # TODO: Get reviews by ISBN not by book
    reviews = Review.objects.filter(book=book)
    review_form = ReviewForm()

    if len(reviews):
        rating = round(sum([float(review.rating) for review in reviews])/len(reviews), 2)
    else:
        rating = "No reviews yet"

    return render_to_response("book.html", context_instance=RequestContext(request,
        {'authenticated': authenticated, 'book': book, 'reviews': reviews, 'review_form': review_form, 'rating':rating} ))


@csrf_exempt
def borrow_book(request, id_book):
    authenticated = False
    borrowed = False
    if request.user.is_authenticated():
        authenticated = True
    book = Book.objects.get(id_book=id_book)
    form = BorrowForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            borrowed_book = form.save(commit=False)
            borrowed_book.book = book
            borrowed_book.user = request.user
            borrowed_book.save()
            borrowed = True


    return render_to_response("book_borrow.html", context_instance=RequestContext(request,
        {'authenticated': authenticated, 'book': book, 'form': form, 'borrowed': borrowed}))


def borrow(request):
    authenticated = False
    if request.user.is_authenticated():
        authenticated = True
    print 'borrow'
    return render_to_response("home.html", {'authenticated': authenticated,
                                                'borrowed': True})

@csrf_exempt
def reserve_book(request, id_book):
    authenticated = False
    reserved = False
    if request.user.is_authenticated():
        authenticated = True
    book = Book.objects.get(id_book=id_book)

    if request.method == 'POST':
        reserve_form = ReserveForm(request.POST)
        if reserve_form.is_valid():
            reserved_book = reserve_form.save(commit=False)
            reserved_book.book = book
            reserved_book.user = request.user
            reserved_book.save()
            reserved = True

    form = ReserveForm()

    return render_to_response("book_reserve.html", context_instance=RequestContext(request,
        {'authenticated': authenticated, 'book': book, 'form': form, 'reserved': reserved}))

def reserve(request):
    authenticated = False
    if request.user.is_authenticated():
        authenticated = True
    print 'reserve'
    return render_to_response("home.html", {'authenticated': authenticated,
                                                'reserved': True})

def home(request):
    authenticated = False
    if request.user.is_authenticated():
        authenticated = True
    distinct_books = Book.objects.values('title', 'author', 'genre', 'ISBN').distinct()
    books = []
    for distinct_book in distinct_books:
        first_book = Book.objects.filter(ISBN=distinct_book['ISBN']).first()
        for check_book in Book.objects.filter(ISBN=first_book.ISBN):
            if not Borrow.objects.filter(book=check_book).exists()\
               or Borrow.objects.filter(date_return__lte=datetime.now().date(), book=check_book).exists():
                first_book = check_book
                break
        books.append(first_book)

    return render_to_response("home.html", {'authenticated': authenticated, 'books': books})


@csrf_exempt
def search(request):
    authenticated = False
    if request.user.is_authenticated():
        authenticated = True

    query_string = ''
    found_books = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        book_query = get_query(query_string, ['title', 'author', 'genre'])
        found_books = Book.objects.filter(book_query).order_by('title')
        return render_to_response("home.html", {'authenticated': authenticated,
                                                'books': found_books})
    else:
        search_results = Book.objects.all()
        if ('title' in request.GET) and request.GET['title'].strip():
            title_string = request.GET['title']
            book_query = get_query(title_string, ['title'])
            search_results = search_results.filter(book_query)
        if ('author' in request.GET) and request.GET['author'].strip():
            author_string = request.GET['author']
            book_query = get_query(author_string, ['author'])
            search_results = search_results.filter(book_query)
        if ('genre' in request.GET) and request.GET['genre'].strip():
            genre_string = request.GET['genre']
            book_query = get_query(genre_string, ['genre'])
            search_results = search_results.filter(book_query)
        found_books = search_results.order_by('title')
        return render_to_response("advanced_search.html", {'authenticated': authenticated,
                                                           'books': found_books})


@csrf_exempt
def login_user(request):
    state = ""
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/home/')
            else:
                state = "Your account is not active, please contact the site admin."
        else:
            state = "Your username and/or password were incorrect."
    return render_to_response('login.html', {'state':state, 'username': username})


@csrf_protect
def register_user(request):
    if request.method == 'POST':
        uform = UserCreationForm(request.POST)
        if uform.is_valid():
            new_user = uform.save()
            return HttpResponseRedirect("/home/")
    else:
        uform = UserCreationForm()
    return render_to_response("register.html", {
        'uform': uform},
        context_instance=RequestContext(request)
    )


def donate(request):
    authenticated = False
    if request.user.is_authenticated():
        authenticated = True

    return render_to_response("book_donate.html", context_instance=RequestContext(request,
        {'authenticated': authenticated}))


def suggest(request):
    authenticated = False
    if request.user.is_authenticated():
        authenticated = True

    return render_to_response("book_suggest.html", context_instance=RequestContext(request,
        {'authenticated': authenticated}))


def show_profile(request):
    authenticated = False
    if request.user.is_authenticated():
        authenticated = True

    return render_to_response("profile.html", context_instance=RequestContext(request,
        {'authenticated': authenticated}))