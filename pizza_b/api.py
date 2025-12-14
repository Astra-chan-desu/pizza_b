from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Pizza, User, Driver, Branch, Order, OrderItem
from .serializers import PizzaSerializer, UserSerializer, DriverSerializer, BranchSerializer, OrderItemSerializer, OrderSerializer
from .routing import Routing
class PizzaViewSet(viewsets.ModelViewSet):
    queryset = Pizza.objects.all() #filters
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = PizzaSerializer
    #@action(detail=True, methods=['post'])
    #def custom_action(self, request, pk=None):
    #    instance = self.get_object()
    #    print('aaaaaaaaaaaaaaa'+instance)
    #    # Логика кастомного действия
    #    return Response({'status': 'success'})




    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        if self.delivery_address != None: 
            found_coordinates = Routing.CoordsFromAddr(self.delivery_address)
        else:
            found_coordinates = self.delivery_coordinates
        
        items_data = self.request.data.get('items', [])
        estimated_time = 30 

        order = serializer.save(
            delivery_coordinates = found_coordinates,
            estimated_delivery_time=estimated_time,
            status='pending'
        )
        

        for item_data in items_data:
            pizza = Pizza.objects.get(id=item_data['pizza'])
            OrderItem.objects.create(
                order=order,
                pizza=pizza,
                quantity=item_data['quantity'],
                price=pizza.cost
            )
        

        self.assign_driver(order)

    def assign_driver(self, order):

        free_drivers = Driver.objects.filter(status='free', is_active=True)
        if free_drivers.exists():
            driver = free_drivers.first()
            order.driver = driver
            order.status = 'assigned'
            order.save()
            driver.status = 'busy'
            driver.save()

    def get_route(self, order):
        destination = order.delivery_coordinates
        current_location = any
        # Return shop if no driver assigned
        if not getattr(order, 'driver', None):
            current_location = order.branch.coordinates
        else: 
            current_location = order.driver.coordinates
        route = Routing.GetRoute(current_location, destination)
        return route
        