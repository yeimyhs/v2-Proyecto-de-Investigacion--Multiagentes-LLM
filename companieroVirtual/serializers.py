from rest_framework import serializers
from .models import Message, Conversation, KnowledgeTopicLearned, SubKnowledge, GeneratedBy

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = '__all__'

class KnowledgeTopicLearnedSerializer(serializers.ModelSerializer):
    class Meta:
        model = KnowledgeTopicLearned
        fields = '__all__'

class SubKnowledgeSerializer(serializers.ModelSerializer):
    knowledge_learned = KnowledgeTopicLearnedSerializer(read_only=True)

    class Meta:
        model = SubKnowledge
        fields = '__all__'

class GeneratedBySerializer(serializers.ModelSerializer):
    subknowledge = SubKnowledgeSerializer(read_only=True)
    message = MessageSerializer(read_only=True)

    class Meta:
        model = GeneratedBy
        fields = '__all__'
