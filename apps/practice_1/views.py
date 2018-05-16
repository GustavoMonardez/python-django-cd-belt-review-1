from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, Book, Review, Author

def index(request):
    return render(request, "practice_1/index.html")

def register(request):
    user = User.objects.validate_registration(request.POST)
    if user["status"]:
        request.session["alias"] = user["obj"].alias
        request.session["id"] = user["obj"].id
        request.session["email"] = user["obj"].email
        request.session["status"] = "registered"
        return redirect("/books")
    else:
        for value in user["obj"].values():
            messages.error(request, value)
        return redirect("/")

def login(request):
    user = User.objects.validate_login(request.POST)
    if user["status"]:
        request.session["alias"] = user["obj"].alias
        request.session["id"] = user["obj"].id
        request.session["email"] = user["obj"].email
        request.session["status"] = "logged in"
        return redirect("/books")
    else:
        for value in user["obj"].values():
            messages.error(request, value)
        return redirect("/")

# profile welcome page
def books(request):
    if "email" not in request.session:
        messages.error(request, "You must be logged in to access this page")
        return redirect("/")

    #context = {"top": Book.objects.all().order_by("-id")[:3],"books": Book.objects.all()}
    context = {"top": Review.objects.all().order_by("-id")[:3],"books": Book.objects.all()}
    
    return render(request, "practice_1/books.html", context)

def logout(request):
    request.session.flush()
    return redirect("/")

# add page
def add(request):
    context = {"authors":Author.objects.all()}
    return render(request, "practice_1/add_book.html", context)

# add book process request
def add_book(request):
    # capture data
    reviewer = User.objects.filter(email=request.session["email"])
    title = request.POST["title"]
    author_name = request.POST["author"]
    if author_name == "default":
        author_name = request.POST["add_author"]
    review = request.POST["review"]
    rating = request.POST["rating"]
    # validate data
    errors = {}
    if len(title) == 0:
        errors["title"] = "Title can't be empty"
    if len(author_name) == 0:
        errors["author_name"] = "Author can't be empty"
    if errors:
        for value in errors:
            messages.error(request, value)
        return redirect("/books/add")
    else:
        # check if author already in database
        author = Author.objects.filter(name=author_name)
        if author:
            author = author[0]
        else:
            author = Author.objects.create(name=author_name)
        book = Book.objects.create(title=title,author=author)
        review = Review.objects.create(content=review,rating=rating,book=book,reviewer=reviewer[0])
        messages.success(request, "Book and review added successfully")
        return redirect("/books")

def show_book(request, number):
    context = {"book": Book.objects.get(id=number)}
    return render(request, "practice_1/show_book.html", context)

def show_user(request, number):
    # context = {"user": User.objects.get(id=number)}
    # Book.objects.filter() distinct
    context = {"user": User.objects.get(id=number)}
    return render(request, "practice_1/user.html", context)

def add_review(request):
    # capture
    reviewer = User.objects.filter(email=request.session["email"])
    review = request.POST["review"]
    rating = request.POST["rating"]
    book_id = request.POST["id"]
    book = Book.objects.get(id=book_id)
    #validate
    if len(review) == 0:
        messages.error(request, "Review can not be empty")
        return redirect("/books/"+book_id)

    Review.objects.create(content=review,rating=rating,book=book,reviewer=reviewer[0])
    messages.success(request, "Successfully added reivew")
    return redirect("/books")
def delete_review(request):
    page = request.POST["page"]
    review_id = request.POST["review_id"]
    Review.objects.get(id=review_id).delete()
    return redirect("/books/"+page)

