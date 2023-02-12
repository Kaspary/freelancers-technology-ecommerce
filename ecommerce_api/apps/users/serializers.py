from django.conf import settings
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type':'password'}, write_only=True)

    class Meta:
        model = settings.AUTH_USER_MODEL
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
        )
        extra_kwargs = {
            'password':{'write_only':True},
            'date_joined':{'read_only':True},
            'last_login':{'read_only':True},
            'is_active':{'read_only':True},
            'is_staff':{'read_only':True},
            'is_superuser':{'read_only':True},
            'username':{'read_only':True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        
        del attrs['confirm_password']
        return attrs

    def create(self, validated_data):
        validated_data['is_staff'] = False
        validated_data['is_active'] = False
        validated_data['username'] = validated_data['email']
        user = super().create(validated_data)
        user.set_password(validated_data.pop('password'))
        user.save()
        return user


class UpdateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ('first_name', 'last_name')
