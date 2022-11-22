from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Person, Image, Document


class PersonSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user_id = self.context['user_id']
        return Person.objects.create(user_id=user_id, **validated_data)

    class Meta:
        model = Person
        fields = '__all__'
        read_only_fields = ('user',)


class ImageSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user_id = self.context['user_id']
        return Image.objects.create(user_id=user_id, **validated_data)

    class Meta:
        model = Image
        fields = '__all__'
        read_only_fields = ('user',)


class DocumentSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user_id = self.context['user_id']
        return Document.objects.create(user_id=user_id, **validated_data)

    class Meta:
        model = Document
        fields = '__all__'
        read_only_fields = ('user',)


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=50, min_length=8, write_only=True)
    repeat_password = serializers.CharField(max_length=50, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'password',
                  'repeat_password'
                  )
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, args):
        email = args.get('email', None)
        password1 = args.get('password', None)
        password2 = args.get('repeat_password', None)

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': ('Пользователь с таким e-mail уже существует!')})

        if password1 != password2:
            raise serializers.ValidationError({'password': ('Пароли не совпадают!')})

        return super().validate(args)

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], password=validated_data['password'],
                                        email=validated_data['email'])
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
