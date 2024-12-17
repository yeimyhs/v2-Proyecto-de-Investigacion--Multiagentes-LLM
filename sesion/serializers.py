from .models import *
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields ="__all__" 
    
    
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'email', 'password', 'foto', 'age', 'name', 'grade', 
            'country', 'department', 'city'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_password(self, value):
        """
        Validar la contraseña utilizando las reglas de validación de Django.
        """
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    def create(self, validated_data):
        """
        Crear un usuario utilizando el método `create_user` de `CustomUserManager`.
        """
        password = validated_data.pop('password')
        user = CustomUser.objects.create_user(password=password, **validated_data)
        return user
    
    
from rest_framework import serializers
from .models import Session, Topic, TopicsRequirement, LearningTechnique, RecommendedTechniques
from .serializers import CustomUserSerializer  # Assuming you have a CustomUserSerializer for the 'CustomUser' model.

class SessionSerializer(serializers.ModelSerializer):
    #user = CustomUserSerializer(read_only=True)  # Assuming CustomUser model has a serializer.
    lista_requerimientos = serializers.SerializerMethodField()
    tecnicas_recomendadas_a_usar_sesion = serializers.SerializerMethodField()
    class Meta:
        model = Session
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['userinfo']  = CustomUserSerializer(source= 'user' , read_only=True)  # Assuming CustomUser model has a serializer.
        
        #self.fields['technique_d'] = LearningTechniqueSerializer(source='technique', read_only=True)

    def get_tecnicas_recomendadas_a_usar_sesion(self, obj):
        tecnicas = RecommendedTechniques.objects.filter(session=obj)
        return RecommendedTechniquesSerializer(tecnicas, many=True).data

    def get_lista_requerimientos(self, obj):
        lista_requerimientos = TopicsRequirement.objects.filter(session=obj)
        return TopicsRequirementSerializer(lista_requerimientos, many=True).data



class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'

class TopicsRequirementSerializer(serializers.ModelSerializer):
    #session = SessionSerializer(read_only=True)
    #topic = TopicSerializer(read_only=True)

    class Meta:
        model = TopicsRequirement
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['topic_d'] = TopicSerializer(source='topic', read_only=True)



class LearningTechniqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningTechnique
        fields = '__all__'

class RecommendedTechniquesSerializer(serializers.ModelSerializer):
    #session_d = SessionSerializer(read_only=True)
    #technique_d = LearningTechniqueSerializer(read_only=True)

    class Meta:
        model = RecommendedTechniques
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['technique_d'] = LearningTechniqueSerializer(source='technique', read_only=True)

