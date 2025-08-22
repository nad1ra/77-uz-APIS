from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied


class SerializerContextMixin:
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class StandardListResponseMixin:
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            "count": len(queryset),
            "next": None,
            "previous": None,
            "results": serializer.data
        })


class SuccessCreateMixin:
    success_message = "Obyekt muvaffaqiyatli qo‘shildi"

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(
            {
                "success": True,
                "message": self.success_message,
                "data": self.get_serializer(instance).data,
            },
            status=status.HTTP_201_CREATED,
        )


class SuccessDeleteMixin:
    success_message = "Obyekt muvaffaqiyatli o‘chirildi"
    not_found_message = "Obyekt topilmadi"

    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            return Response(
                {"success": True, "message": self.success_message},
                status=status.HTTP_204_NO_CONTENT,
            )
        except self.queryset.model.DoesNotExist:
            return Response(
                {"success": False, "message": self.not_found_message},
                status=status.HTTP_404_NOT_FOUND,
            )


class UserFilteredQuerysetMixin:
    user_field = "user"

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return self.queryset.none()
        return self.queryset.filter(**{self.user_field: self.request.user})


class OwnerProtectedDeleteMixin:
    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("Siz bu obyektni o‘chira olmaysiz.")
        instance.delete()
