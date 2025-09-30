from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem
from .serializers import OrderSerializer, CreateOrderSerializer
from ..firebase_service import initialize_firebase, send_notification_to_topic

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateOrderSerializer
        return OrderSerializer

    def create(self, request, *args, **kwargs):
        # Initialize Firebase
        initialize_firebase()

        # Get items from request data
        items = request.data.get('items', [])

        # Create serializer with items context
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Create order with items
        self.perform_create(serializer, items)

        headers = self.get_success_headers(serializer.data)

        # Send notification to admin
        self.send_admin_notification(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, items=None):
        serializer.save(items=items)

    def send_admin_notification(self, order_data):
        try:
            from django.contrib.auth import get_user_model
            from notifications.views import create_notification
            User = get_user_model()

            # Get admin users
            admin_users = User.objects.filter(is_staff=True)

            # Prepare notification data
            notification_data = {
                'order_id': str(order_data['id']),
                'customer_name': order_data['customer_name'],
                'total': str(order_data['total']),
                'type': 'new_order'
            }

            # Create notification for each admin user
            for admin in admin_users:
                create_notification(
                    recipient=admin,
                    type='new_order',
                    title='طلب جديد',
                    message=f'طلب جديد من {order_data["customer_name"]} بقيمة {order_data["total"]} د.ع',
                    data=notification_data
                )

            # Also send notification to admin topic (for backward compatibility)
            send_notification_to_topic(
                topic='admin_orders',
                title='طلب جديد',
                body=f'طلب جديد من {order_data["customer_name"]} بقيمة {order_data["total"]} د.ع',
                data=notification_data
            )
        except Exception as e:
            print(f"Error sending admin notification: {str(e)}")

    @action(detail=False, methods=['post'])
    def register_admin_token(self, request):
        """Register admin device token for notifications"""
        try:
            token = request.data.get('token')
            if not token:
                return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)

            # Initialize Firebase
            initialize_firebase()

            # Subscribe the token to admin topic
            from ..firebase_service import subscribe_to_topic
            subscribe_to_topic([token], 'admin_orders')

            return Response({'success': 'Token registered successfully'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        