import base64
import uuid

from deals.models import Bid, Deal, Message, Payment, Picture, Product
from django.core.files.base import ContentFile
from django.db import transaction
from rest_framework import serializers
from users.serializers import AddressSerializer


class PictureSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Picture
        fields = ("image", "product")

    def to_internal_value(self, data):
        try:
            image_string = data.pop("image", None)
            content_file = self._base64_to_content_file(image_string)
            return super().to_internal_value({"image": content_file, **data})
        except Exception as e:
            raise serializers.ValidationError({"image": e})

    def _base64_to_content_file(self, image_string):
        if not image_string:
            return
        b64, ext = self._parse_base64(image_string)
        return ContentFile(b64, name=f"{uuid.uuid4()}.{ext}")

    def _parse_base64(self, image_string):
        assert ";base64," in image_string, "Invalid base64 format"
        format, imgstr = image_string.split(";base64,")
        ext = format.split("/")[-1]
        return base64.b64decode(imgstr), ext


class PictureField(serializers.SlugRelatedField):
    def to_internal_value(self, data):
        return data

    def to_representation(self, data):
        request = self.context.get("request")
        if not (data.image and request):
            return None

        return request.build_absolute_uri(data.image.url)


class ProductSerializer(serializers.ModelSerializer):
    pictures = PictureField(
        many=True,
        slug_field="image",
        queryset=Picture.objects.all(),
        help_text='Base64 format, e.g. "data:image/jpg;base64,/9j/2wBDAA..."'
    )

    class Meta:
        model = Product
        fields = ("__all__")

    def create(self, validated_data):
        with transaction.atomic():
            pictures = validated_data.pop("pictures", [])
            product = super().create(validated_data)
            self.save_pictures(product.id, pictures)
            return product
        
    def update(self, instance, validated_data):
        with transaction.atomic():
            pictures = validated_data.pop("pictures", [])
            product = super().update(instance, validated_data)
            self.save_pictures(product.id, pictures)
            return product

    def save_pictures(self, product_id, pictures):
        for image in pictures:
            picture = PictureSerializer(data={"product": product_id, "image": image})
            picture.is_valid(raise_exception=True)
            picture.save()


class DealSerializer(serializers.ModelSerializer):
    location = AddressSerializer()
    product = ProductSerializer()

    class Meta:
        model = Deal
        exclude = ("user",)

    def create(self, validated_data):
        with transaction.atomic():
            location = AddressSerializer(data=validated_data.pop("location"))
            location.is_valid(raise_exception=True)
            location = location.save()

            product = ProductSerializer(data=validated_data.pop("product"))
            product.is_valid(raise_exception=True)
            product = product.save()

            validated_data.update({
                "user": self.context["user"],
                "location": location,
                "product": product
            })
            deal = super().create(validated_data)
            return deal
        
    def update(self, instance, validated_data):
        with transaction.atomic():
            location = AddressSerializer(data=validated_data.pop("location"), instance=instance.location)
            location.is_valid(raise_exception=True)
            location = location.save()

            product = ProductSerializer(data=validated_data.pop("product"), instance=instance.product)
            product.is_valid(raise_exception=True)
            product = product.save()

            validated_data.update({
                "location": location,
                "product": product
            })
            deal = super().update(instance, validated_data)
            return deal


class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = (
            "id",
            "accepted",
            "value",
            "description",
            "user",
            "created_at",
            "updated_at",
        )
        extra_kwargs = {"user": {"read_only": True}}

    def create(self, validated_data):
        deal_id = self.context["deal_id"]
        try:
            deal = Deal.objects.get(id=deal_id)
        except Deal.DoesNotExist:
            raise serializers.ValidationError(
                {"deal_id": [f"Deal was not found with id {deal_id}."]}
            )

        validated_data.update({"user": self.context["user"], "deal": deal})
        return super().create(validated_data)


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ("id", "title", "message", "user", "created_at", "updated_at")
        extra_kwargs = {"user": {"read_only": True}}

    def create(self, validated_data):
        deal_id = self.context["deal_id"]
        try:
            deal = Deal.objects.get(id=deal_id)
        except Deal.DoesNotExist:
            raise serializers.ValidationError(
                {"deal_id": [f"Deal was not found with id {deal_id}."]}
            )

        validated_data.update({"user": self.context["user"], "deal": deal})
        return super().create(validated_data)


class DeliverySerializer(serializers.Serializer):
    code = serializers.CharField(help_text="Código do Serviço de Entrega.")
    value = serializers.FloatField(
        help_text="Preço total da encomenda, em Reais, incluindo os preços dos serviços opcionais"
    )
    own_hand_value = serializers.FloatField(
        help_text="Preço do serviço adicional Mão Própria"
    )
    value_notice_receipt = serializers.FloatField(
        help_text="Preço do serviço adicional Aviso de Recebimento"
    )
    declared_value = serializers.FloatField(
        help_text="Preço do serviço adicional Valor Declarado"
    )
    deadline = serializers.IntegerField(help_text="Prazo de entrega")
    value_without_additionals = serializers.FloatField(help_text="Valor sem adicionais")
    home_delivery = serializers.BooleanField(help_text="Entrega domiciliar")
    delivery_in_saturday = serializers.BooleanField(help_text="Entrega sabado")


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
