from django.apps import AppConfig


class BooksConfig(AppConfig):
    name = 'books'

    def ready(self):
        from auditlog.registry import auditlog
        from .models import Book, Category
        import books.signals

        auditlog.register(Book)
        auditlog.register(Category)
