from rest_framework import serializers
from borrow.models import Borrow


class BorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrow
        fields = '__all__'
        read_only_fields = (
            'borrow_date', 'due_date', 'return_date', 'fine_amount', 'is_returned'
        )