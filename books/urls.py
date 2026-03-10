from django.urls import path
from .views import *


urlpatterns = [
    # author urls
    path("authors/", AuthorListCreateView.as_view(), name="authors"),
    path("authors/<int:id>/", AuthorDetailView.as_view(), name="author-detail"),

    # publisher urls
    path("publishers/create/", PublisherCreateView.as_view(), name="publisher_create"),
    path("publishers/", PublisherListView.as_view(), name="publishers"),
    path("publishers/detail/<int:publisher_id>/", PublisherDetailView.as_view(), name="publisher_detail"),
    path("publishers/update/<int:publisher_id>/", PublisherUpdateView.as_view(), name="publisher_update"),
    path("publishers/delete/<int:publisher_id>/", PublisherDeleteView.as_view(), name="publisher_delete"), 

    # category urls
    path("categories/", CategoryListCreateView.as_view(), name="categories"),
    path("categories/<int:id>/", CategoryRetrieveUpdateDeleteView.as_view()),

    # book urls
    path("books/create", BookCreateAPIView.as_view()),
    path("books/", BookListAPIView.as_view(),),
    path("books/<int:id>/", BookRetrieveUpdateDestroyAPIView.as_view(),),

    # book_copy urls
    path("bookcopies/", BookListCreateView.as_view()),
    path("bookcopies/<int:id>/", BookCopyRetrieveUpdateDestroyAPIView.as_view(),),
]
