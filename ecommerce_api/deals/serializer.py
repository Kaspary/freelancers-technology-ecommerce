import base64
import uuid

from deals.models import Deals, Picture
from django.core.files.base import ContentFile
from django.db import transaction
from rest_framework import serializers
from users.models import Address
from users.serializers import AddressSerializer


class PictureSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Picture
        fields = ("image", "deals")

    def to_internal_value(self, data):
        image_data = data.pop("image", None)
        if image_data != None:
            format, imgstr = image_data.split(";base64,")
            ext = format.split("/")[-1]
            content_file = ContentFile(
                base64.b64decode(imgstr), name=f"{uuid.uuid4()}.{ext}"
            )
        return super().to_internal_value({"image": content_file, **data})


class PictureField(serializers.SlugRelatedField):
    def to_internal_value(self, data):
        return data

    def to_representation(self, data):
        request = self.context.get("request")
        if not (data.image and request):
            return None

        return request.build_absolute_uri(data.image.url)


class NegotiatonSerializer(serializers.ModelSerializer):
    location = AddressSerializer()
    pictures = PictureField(
        many=True, slug_field="image", queryset=Picture.objects.all()
    )

    class Meta:
        model = Deals
        fields = "__all__"

    def create(self, validated_data):
        with transaction.atomic():
            images_data = validated_data.pop("pictures", [])

            location_data = validated_data.pop("location", None)
            if location_data:
                location = Address.objects.create(**location_data)

            validated_data["location"] = location
            deal = super().create(validated_data)
            for image in images_data:
                picture = PictureSerializer(data={"deals": deal.id, "image": image})
                picture.is_valid(raise_exception=True)
                picture.save()
            return deal


class NegotiatonResultSerializer(serializers.Serializer):
    deal = NegotiatonSerializer()
