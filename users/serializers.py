from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Users

# Serializer pour l'inscription
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = Users
        fields = ['firstname', 'lastname', 'email', 'phone', 'profil_image', 'password']

    def create(self, validated_data):
        user = Users.objects.create_user(**validated_data)
        return user


# Serializer pour le login
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Email ou mot de passe incorrect")
        data['user'] = user
        return data


# Serializer pour le changement de mot de passe
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=6)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("L'ancien mot de passe est incorrect")
        return value

# update user

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        # Tu peux mettre tous les champs que l’utilisateur peut mettre à jour
        fields = ['firstname', 'lastname', 'phone', 'profil_image']
        extra_kwargs = {
            'firstname': {'required': False},
            'lastname': {'required': False},
            'phone': {'required': False},
            'profil_image': {'required': False},
        }

    def update(self, instance, validated_data):
        # Mettre à jour chaque champ si présent dans validated_data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'firstname', 'lastname', 'email', 'phone', 'profil_image']
        read_only_fields = ['id', 'email']  # L’email et l’ID ne sont pas modifiables