from django.db import transaction
from django.utils import timezone
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from bookings.models import Booking
from payments.models import Payment, PaymentStatus, PaymentType
from payments.serializers import PaymentSerializer, PaymentListSerializer, PaymentDetailSerializer
from payments.stripe_service import create_stripe_session


class PaymentViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Payment.objects.select_related("booking").all().order_by("-id")
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == "list":
            return PaymentListSerializer
        if self.action == "retrieve":
            return PaymentDetailSerializer
        return PaymentSerializer
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        booking_id = request.data.get("booking")
        payment_type = request.data.get("payment_type", PaymentType.PAYMENT)
        booking = Booking.objects.get(id=booking_id)
        session_data = create_stripe_session(booking, payment_type, request)
        payment = Payment.objects.create(
            booking=booking,
            amount=session_data["amount"],
            status=PaymentStatus.PENDING,
            payment_type=payment_type,
            session_url=session_data["session_url"],
            session_id=session_data["session_id"]
        )
        serializer = self.get_serializer(payment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PaymentSuccessView(APIView):
    def get(self, request, *args, **kwargs):
        session_id = request.GET.get("session_id")
        payment = Payment.objects.filter(session_id=session_id).first()
        if payment:
            payment.status = PaymentStatus.PAID
            payment.paid_at = timezone.now()
            payment.save()
            return Response({"status": "success"})
        return Response({"status": "not found"}, status=404)


class PaymentCancelView(APIView):
    def get(self, request, *args, **kwargs):
        session_id = request.GET.get("session_id")
        payment = Payment.objects.filter(session_id=session_id).first()
        if payment:
            payment.status = PaymentStatus.CANCELLED
            payment.save()
            return Response({"status": "cancelled"})
        return Response({"status": "not found"}, status=404)
