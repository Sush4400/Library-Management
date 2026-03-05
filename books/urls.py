from django.urls import path
from .views import *


urlpatterns = [
    # author urls
    path("authors/", AuthorListView.as_view(), name="authors"),
    path("authors/", AuthorCreateView.as_view(), name="author_create"),
    path("authors/<int:author_id>/", AuthorDetailView.as_view(), name="author_detail"),
    path("authors/<int:author_id>/", AuthorUpdateView.as_view(), name="author_update"),
    path("authors/<int:author_id>/", AuthorDeleteView.as_view(), name="author_delete"),

    # publisher urls
    path("publishers/", PublisherCreateView.as_view(), name="publisher_create"),
    path("publishers/", PublisherListView.as_view(), name="publishers"),
    path("publishers/<int:publisher_id>/", PublisherDetailView.as_view(), name="publisher_detail"),
    path("publishers/<int:publisher_id>/", PublisherUpdateView.as_view(), name="publisher_update"),
    path("publishers/<int:publisher_id>/", PublisherDeleteView.as_view(), name="publisher_delete"),

    # category urls
    path("categories/", CategoryCreateView.as_view(), name="category_create"),
    path("categories/", CategoryListView.as_view(), name="categories"),
    path("categories/<int:category_id>/", CategoryUpdateView.as_view(), name="category_update"),
    path("categories/<int:category_id>/", CategoryDeleteView.as_view(), name="category_delete"),

    # book urls
    path("books/", BooksListView.as_view(), name="books"),

    # book_copy urls
]
