from rest_framework.serializers import ModelSerializer

from .models import Person, TrustRelation


class PersonSerializer(ModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'name', 'topics']
        read_only_fields = ['id']


class TrustRelationSerializer(ModelSerializer):
    class Meta:
        model = TrustRelation
        fields = ['trust_level', 'relation_person']