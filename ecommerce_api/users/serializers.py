from rest_framework import serializers
from django.db import transaction
from delivery.serializers import AddressSerializer
from delivery.models import Address

from users.models import Invite, User


class UserSerializer(serializers.ModelSerializer):
    location = AddressSerializer(required=True)
    confirm_password = serializers.CharField(style={'input_type':'password'}, write_only=True)
    invite = serializers.SlugRelatedField(required=False, allow_null=True, write_only=True, slug_field='id', queryset=Invite.objects.all())

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
            'location',
            'invite'
        )
        extra_kwargs = {
            'date_joined':{'read_only':True},
            'last_login':{'read_only':True},
            'is_active':{'read_only':True},
            'is_staff':{'read_only':True},
            'is_superuser':{'read_only':True},
            'password':{'write_only':True},
        }

    def validate(self, attrs):
        erros = {}
        if attrs['password'] != attrs['confirm_password']:
            erros['password'] = 'Passwords must match.'
        
        if attrs['invite'] and attrs['invite'].user_invited:
            erros['invite'] = 'This invitation has already been used.'

        if erros:
            raise serializers.ValidationError(erros)
        
        del attrs['confirm_password']
        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            invite = validated_data.pop('invite', None)

            validated_data["location"] = self._save_location(
                validated_data.pop('location')
            )

            user = self._save_user(validated_data)
            self._update_invite(invite, user)
            return user
    
    def _update_invite(self, invite, user):
        if not invite: return invite
        invite.user_invited = user
        invite.save()
        return invite

    def _save_location(self, data):
        location = AddressSerializer(data=data)
        location.is_valid(raise_exception=True)
        location = location.save()
        return Address.objects.create(**data)
            
    def _save_user(self, data):
        user = super().create(data)
        user.set_password(data.pop('password'))
        user.save()
        return user


class UpdateUserSerializer(serializers.ModelSerializer):
    location = AddressSerializer(required=True)
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
            'location',
            'date_joined',
            'last_login',
            'is_active',
            'is_staff',
            'is_superuser'
        )

        extra_kwargs = {
            'date_joined':{'read_only':True},
            'last_login':{'read_only':True},
            'is_active':{'read_only':True},
            'is_staff':{'read_only':True},
            'is_superuser':{'read_only':True},
            'id':{'read_only':True},
            'username':{'read_only':True},
            'email':{'read_only':True},
            'password':{'write_only':True},
        }

    def validate(self, attrs):
        erros = {}
        if attrs['password'] != attrs['confirm_password']:
            erros['password'] = 'Passwords must match.'
        
        if erros:
            raise serializers.ValidationError(erros)
        
        del attrs['confirm_password']
        return attrs
    
    def update(self, instance, validated_data):
        with transaction.atomic():
            validated_data["location"] = self._save_location(
                validated_data.pop('location'), instance.location
            )
            user = super().update(instance, validated_data)
            user.set_password(validated_data.pop('password'))
            user.save()
            return user

    def _save_location(self, data,instance):
        location = AddressSerializer(data=data, instance=instance)
        location.is_valid(raise_exception=True)
        location = location.save()
        return Address.objects.create(**data)

class InviteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Invite
        fields = (
            'id',
            'name',
            'email',
            'user_invited',
            'created_at',
            'updated_at'
        )
        extra_kwargs = {
            'user_invited':{'read_only':True}
        }

    def create(self, validated_data):
        validated_data.update({
            'user': self.context['user'],
        })
        return super().create(validated_data)
