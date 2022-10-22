from django.shortcuts import render
from rest_framework import viewsets, status
from oAuth.models import NewUser, Books
from rest_framework.response import Response
from oAuth.serializers import UserSerializer, Bookerializer
from django.db.models import Q
from djangoTest2.settings import BASE_URL
from django.core.mail import send_mail


# Create your views here.

class UserInfoViewSet(viewsets.ViewSet):
    queryset = NewUser.objects.all().order_by('-date_joined')
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        print('ok')
        user_info = NewUser.objects.filter(id=request.user.id).values()[0]
        print(user_info)
        role = request.user.roles
        if role == 0:
            user_info['roles'] = ['admin']
        else:
            user_info['roles'] = ['user']

        return Response(user_info)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Books.objects.all()
    serializer_class = Bookerializer

    def list(self, request, *args, **kwargs):
        # self.queryset = self.queryset.filter(~Q(is_delete=True))
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.is_delete = True
        print('ok')
        instance.save()
        # instance.delete()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = NewUser.objects.all()
    serializer_class = UserSerializer

    # list :get
    # create: post
    # put: update(整体更新，提供所有更改后的字段信息)
    # patch：partial_update(据不更新，仅提供需要修改的信息)
    # delete: destroy
    # get_id: retrieve

    def list(self, request, *args, **kwargs):
        user = request.user
        # if 'roles' in user and user.roles == 1:
        #         self.queryset = self.queryset.filter(~Q(username='admin'))
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class UserCreateViewSet(viewsets.ModelViewSet):
    queryset = NewUser.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['post', 'get']
    permission_classes = []

    def retrieve(self, request, *args, **kwargs):
        instance = NewUser.objects.get(code=kwargs['pk'])
        instance.is_active = True
        instance.save()
        data = {
            'status': 'success',
        }
        return Response(data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_info = self.perform_create(serializer)
        user_info.set_password(request.data['password'])
        user_info.is_active = False
        user_info.save()
        code = user_info.code
        # url = request.build_absolute_uri("/api/user_activate/" + str(code) + "/")
        url = BASE_URL + "/#/user_activate?code=" + str(code)
        print(url)

        send_mail(
            '用户激活',
            url,
            'xtlyk@163.com',
            [user_info.email],
            fail_silently=False,
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()
