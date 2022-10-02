from rest_framework.serializers import ModelSerializer

from .models import Person, TrustRelation, Message


class TrustRelationSerializer(ModelSerializer):
    class Meta:
        model = TrustRelation
        fields = ['trust_level', 'relation_person']


class PersonSerializer(ModelSerializer):

    class Meta:
        model = Person
        fields = ['name', 'topics']


class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = ['sender', 'text']