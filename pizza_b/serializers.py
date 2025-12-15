from rest_framework import serializers
from .models import Pizza, User, Branch, Driver, Order, OrderItem

class PizzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pizza
        fields = '__all__'
    
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'

class DriverSerializer(serializers.ModelSerializer):
    branch = BranchSerializer(read_only=True)  # Можно оставить только для отображения или добавить write-поддержку
    branch_id = serializers.PrimaryKeyRelatedField(
        queryset=Branch.objects.all(),
        source='branch',
        write_only=True,
        required=False
    )
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    class Meta:
        model = Driver
        fields = ['id', 'name', 'phone_number', 'status', 'coordinates', 'branch', 'branch_id', 'status_display']



class OrderItemSerializer(serializers.ModelSerializer):
    pizza_name = serializers.CharField(source='pizza.name', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['pizza', 'pizza_name', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, source='orderitem_set')
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    total_cost = serializers.SerializerMethodField()

    driver_name = serializers.CharField(source='driver.name', read_only=True)
    branch_address = serializers.CharField(source='branch.address', read_only=True)  
    user_name = serializers.CharField(source='user.name', read_only=True)
    class Meta:
        model = Order
        fields = [
            'id', 'customer_phone', 'delivery_address', 'delivery_coordinates',
            'total_cost', 'status', 'status_display', 'estimated_delivery_time',
            'created_at', 'updated_at', 'driver', 'branch', 'items', 'user_name', 'branch_address', 'driver_name',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'status_display']
    def get_total_cost(self, obj):
        return sum(item.quantity * item.price for item in obj.orderitem_set.all())