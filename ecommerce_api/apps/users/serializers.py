from rest_framework import serializers
from django.contrib.auth.models import User

from apps.users.models import Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ('user',)


class UserSerializer(serializers.ModelSerializer):
    location = AddressSerializer()
    confirm_password = serializers.CharField(style={'input_type':'password'}, write_only=True)

    class Meta:
        model = User
        fields = (
        	'id', 
        	'username',
        	'email',
            'password',
            'confirm_password',
        	'first_name', 
        	'last_name', 
        	'is_active', 
        	'is_staff', 
        	'is_superuser', 
        	'date_joined', 
        	'last_login',
            'location'
        )
        extra_kwargs = {
            'date_joined':{'read_only':True},
            'last_login':{'read_only':True},
            'is_active':{'read_only':True},
            'is_staff':{'read_only':True},
            'is_superuser':{'read_only':True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        
        del attrs['confirm_password']
        return attrs

    def create(self, validated_data):
        validated_data['is_staff'] = False
        validated_data['is_active'] = True
        address_data = validated_data.pop('address')
        user = super().create(validated_data)
        user.set_password(validated_data.pop('password'))
        user.save()
        if address_data:
            Address.objects.create(user=user, **address_data)
        return user
