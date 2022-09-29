from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_200_OK
from rest_framework.views import APIView

from .models import Person, Topic, PersonTopic, TrustRelation
from .serializers import PersonSerializer, TrustRelationSerializer


class PersonView(APIView):
    def post(self, request):
        print(request.data)
        if request.data.get('topics') != None:
            topic_list = []
            for topic_name in request.data.get('topics'):
                topic, created = Topic.objects.get_or_create(name=topic_name)
                topic_list.append(topic)
        else:
            return JsonResponse({'Response': 400, 'Errors': {"topics": ["This field is required"]}},
                                status=HTTP_400_BAD_REQUEST)

        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            person, _ = Person.objects.get_or_create(name=serializer.validated_data.get('name'))

            for topic in topic_list:
                person_topic, _ = PersonTopic.objects.get_or_create(topic=topic, person=person)
        else:
            return JsonResponse({'Response': 400, 'Errors': serializer.errors}, status=HTTP_400_BAD_REQUEST)
        return JsonResponse({'Response': 201}, status=HTTP_201_CREATED)

    def get(self, request):
        queryset = Person.objects.all()
        serializer = PersonSerializer(queryset, many=True)
        return Response(serializer.data)


class TrustConnectionsView(APIView):
    def post(self, request, pk):
        status = HTTP_200_OK
        for person_id, trust_level in request.data.items():
            json_format = {'trust_level': trust_level, 'relation_person': int(person_id)}
            serializer = TrustRelationSerializer(data=json_format)
            if serializer.is_valid():
                person = Person.objects.get(id=pk)
                trust_relation = TrustRelation.objects.filter(person=person,
                                                              relation_person=serializer.validated_data.get(
                                                                  'relation_person')).first()
                if trust_relation == None:
                    trust_relation = TrustRelation.objects.create(trust_level=serializer.validated_data.get('trust_level'),
                                                                  relation_person=serializer.validated_data.get(
                                                                      'relation_person'), person=person)
                    status = HTTP_201_CREATED
                else:
                    trust_relation.trust_level = serializer.validated_data.get('trust_level')
                    trust_relation.save()
            else:
                return JsonResponse({'Response': 400, 'Errors': serializer.errors}, status=HTTP_400_BAD_REQUEST)
        if status == HTTP_201_CREATED:
            return JsonResponse({'Response': 201}, status=status)
        return JsonResponse({'Response': 200}, status=status)

    def get(self, request, pk):
        queryset = TrustRelation.objects.filter(person_id=pk)
        serializer = TrustRelationSerializer(queryset, many=True)
        return Response(serializer.data)
