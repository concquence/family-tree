from django.contrib import admin
from rest_framework import viewsets, status
from rest_framework.response import Response
from .permissions import IsAuthenticatedAndOwner


class ViewSetMixin(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedAndOwner,)

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}

    def get_queryset(self):
        user_queryset = self.queryset.filter(user=self.request.user)
        return user_queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        user_queryset = self.queryset.filter(user=self.request.user)
        serializer = self.get_serializer(user_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data,
                                         partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        user_queryset = self.queryset.filter(user=self.request.user)
        serializer = self.get_serializer(user_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        item = self.get_object()
        item.delete()
        user_queryset = self.queryset.filter(user=self.request.user)
        serializer = self.get_serializer(user_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdminMixin(admin.ModelAdmin):
    exclude = ('user',)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)
