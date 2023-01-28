from rest_framework import serializers

from shop.models import Store, Location, Product
from shop.serializers.location import LocationSerializer
from shop.serializers.product import ProductSerializer


class StoreSerializer(serializers.ModelSerializer):

    location = serializers.ManyRelatedField(child_relation=LocationSerializer())
    product = serializers.ManyRelatedField(child_relation=ProductSerializer())

    def create(self, data):
        if data['level'] == 0 and data['supplier']:
            raise serializers.ValidationError('Завод не может иметь поставщика')

        location_data = data.pop('location')
        product_data = data.pop('product')

        data['location'] = []
        data['product'] = []

        for location in location_data:
            location_object, _ = Location.objects.get_or_create(**location)
            data['location'].append(location_object.pk)

        for product in product_data:
            product_object, _ = Product.objects.get_or_create(**product)
            data['product'].append(product_object.pk)

        return super().create(data)

    def update(self, instance, data):
        if data['level'] == 0 and data['supplier']:
            raise serializers.ValidationError('Завод не может иметь поставщика')

        location_data = data.pop('location')
        product_data = data.pop('product')
        data['location'] = []
        data['product'] = []

        for location in location_data:
            location_object, _ = Location.objects.get_or_create(**location)
            data['location'].append(location_object.pk)

        for product in product_data:
            product_object, _ = Product.objects.get_or_create(**product)
            data['product'].append(product_object.pk)

        return super().update(instance, data)

    class Meta:
        model = Store
        fields = '__all__'
        read_only_fields = ['created', 'debt']

