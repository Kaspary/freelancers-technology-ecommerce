from rest_framework import serializers
from django.db import transaction
from delivery.serializers import AddressSerializer
from delivery.models import Address

from users.models import Invite, User


class UserSerializer(serializers.ModelSerializer):
    location = AddressSerializer()
    confirm_password = serializers.CharField(style={'input_type':'password'}, write_only=True)
    invite = serializers.SlugRelatedField(write_only=True, slug_field='id', queryset=Invite.objects.all())

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
        }

    def validate(self, attrs):
        erros = {}
        if attrs['password'] != attrs['confirm_password']:
            erros['password'] = 'Passwords must match.'
        
        if attrs['invite'].user_invited:
            erros['invite'] = 'This invitation has already been used.'

        if erros:
            raise serializers.ValidationError(erros)
        
        del attrs['confirm_password']
        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            invite = validated_data.pop('invite', None)

            validated_data["location"] = self._save_location(
                validated_data.pop('location', None)
            )

            user = self._save_user(validated_data)
            self._update_invite(invite, user)
            return user
    
    def _update_invite(self, invite, user):
        invite.user_invited = user
        invite.save()
        return invite

    def _save_location(self, data):
        if data:
            return Address.objects.create(**data)
            
    def _save_user(self, data):
        user = super().create(data)
        user.set_password(data.pop('password'))
        user.save()
        return user


class InviteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Invite
        fields = (
            'name',
            'email'
        )

    def create(self, validated_data):
        validated_data.update({
            'user': self.context['user'],
        })
        return super().create(validated_data)
