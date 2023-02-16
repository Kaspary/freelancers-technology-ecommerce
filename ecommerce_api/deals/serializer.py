import uuid

from deals.models import Bid, Deal, Picture
from django.core.files.base import ContentFile
from django.db import transaction
from rest_framework import serializers
from users.models import Address
from users.serializers import AddressSerializer


class PictureSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Picture
        fields = ("image", "deal")

    def to_internal_value(self, data):
        image_string = data.pop("image", None)
        content_file = self.base64_to_content_file(image_string)
        return super().to_internal_value({"image": content_file, **data})

    def base64_to_content_file(self, image_string):
        if not image_string:
            return
        b64, ext = self.parse_base64(image_string)
        return ContentFile(b64, name=f"{uuid.uuid4()}.{ext}")

    def parse_base64(self, image_string):
        format, imgstr = image_string.split(";base64,")
        ext = format.split("/")[-1]
        return image_string.b64decode(imgstr), ext


class PictureField(serializers.SlugRelatedField):
    def to_internal_value(self, data):
        return data

    def to_representation(self, data):
        request = self.context.get("request")
        if not (data.image and request):
            return None

        return request.build_absolute_uri(data.image.url)


class DealSerializer(serializers.ModelSerializer):
    location = AddressSerializer()
    pictures = PictureField(
        many=True, slug_field="image", queryset=Picture.objects.all()
    )

    class Meta:
        model = Deal
        exclude = ("user",)

    def create(self, validated_data):
        with transaction.atomic():
            pictures = validated_data.pop("pictures", [])

            location_data = validated_data.pop("location", None)
            if location_data:
                location = Address.objects.create(**location_data)

            validated_data.update({
                'user': self.context['user'],
                'location': location
            })
            deal = super().create(validated_data)
            self.save_pictures(deal.id, pictures)
            
            return deal

    def save_pictures(self, deal_id, pictures):
        for image in pictures:
                picture = PictureSerializer(data={"deal": deal_id, "image": image})
                picture.is_valid(raise_exception=True)
                picture.save()


class DealResultSerializer(serializers.Serializer):
    deal = DealSerializer()


class BidSerializer(serializers.ModelSerializer):

    user_id = serializers.CharField(source='user', read_only=True)

    class Meta:
        model = Bid
        fields = (
            'id',
            'accepted',
            'value',
            'description',
            'user_id',
            'created_at',
            'updated_at',
        )

    def create(self, validated_data):
        deal_id = self.context['deal_id']
        try:
            deal = Deal.objects.get(id=deal_id)
        except Deal.DoesNotExist:
            raise serializers.ValidationError({"deal_id": [f'Deal was not found with id {deal_id}.']})

        validated_data.update({
            'user': self.context['user'],
            'deal': deal
        })
        return super().create(validated_data)
