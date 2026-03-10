from django.shortcuts import render
from django.db.models import Avg

def update_book_rating(book):
    avg = book.reviews.aggregate(avg=Avg("rating"))["avg"] or 0
    book.average_rating = avg
    book.save(update_fields=["average_rating"])