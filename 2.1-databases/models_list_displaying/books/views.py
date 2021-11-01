from django.shortcuts import render
from django.core.paginator import Paginator

from books.models import Book


def books_view(request):
    template = 'books/books_list.html'
    books = Book.objects.all()
    context = {
        'books': books,
    }
    return render(request, template, context)


def get_book_by_date(request, pub_date):
    template = 'books/books_list.html'
    library = Book.objects.all().order_by('pub_date')
    book = library.get(pub_date=pub_date)

    for index, item in enumerate(library):
        if item == book:
            num_page_book = index + 1
            break

    paginator = Paginator(library, 1)
    page = paginator.get_page(num_page_book)

    context = {
        'book': book,
    }

    if page.has_previous():
        index = page.previous_page_number() - 1
        context['previous_book'] = library[index].pub_date
    if page.has_next():
        index = page.next_page_number() - 1
        context['next_book'] = library[index].pub_date

    return render(request, template, context)
