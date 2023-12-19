from rest_framework import serializers
from .models import Product, ProductCategory, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = []


class ProductCategorySerializer(serializers.ModelSerializer):

    category = CategorySerializer()

    class Meta:
        model = ProductCategory
        exclude = []


class ProductSerializer(serializers.ModelSerializer):

    categories = ProductCategorySerializer(many=True, source="categories_pivot")

    class Meta:
        model = Product
        exclude = []
        depth = 1
