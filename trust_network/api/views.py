from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_200_OK
from rest_framework.views import APIView

from .models import Person, Topic, PersonTopic, TrustRelation, Message
from .serializers import PersonSerializer, TrustRelationSerializer, MessageSerializer


class PersonView(APIView):
    def post(self, request):
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
            topic_names_list = []
            for topic in topic_list:
                person_topic, _ = PersonTopic.objects.get_or_create(topic=topic, person=person)
                topic_names_list.append(topic.name)

        else:
            return JsonResponse({'Response': 400, 'Errors': serializer.errors}, status=HTTP_400_BAD_REQUEST)
        return JsonResponse({'id': person.id, "topics": topic_names_list}, status=HTTP_201_CREATED)


class TrustConnectionsView(APIView):
    def post(self, request, pk):
        for person_id, trust_level in request.data.items():
            json_format = {'trust_level': trust_level, 'relation_person': int(person_id)}
            serializer = TrustRelationSerializer(data=json_format)
            if serializer.is_valid():
                person = Person.objects.get(id=pk)
                trust_relation = TrustRelation.objects.filter(person=person,
                                                              relation_person=serializer.validated_data.get(
                                                                  'relation_person')).first()
                if trust_relation == None:
                    trust_relation = TrustRelation.objects.create(
                        trust_level=serializer.validated_data.get('trust_level'),
                        relation_person=serializer.validated_data.get('relation_person'), person=person)
                else:
                    trust_relation.trust_level = serializer.validated_data.get('trust_level')
                    trust_relation.save()
            else:
                return JsonResponse({'Response': 400, 'Error': serializer.errors}, status=HTTP_400_BAD_REQUEST)
        return Response(status=HTTP_201_CREATED)


class MessageView(APIView):
    def post(self, request):
        if {'text', 'topics', 'from_person_id', 'min_trust_level'}.issubset(request.data):
            json_format = {"text": request.data.get('text'), "sender": request.data.get('from_person_id')}
            serializer = MessageSerializer(data=json_format)
            if serializer.is_valid():
                sender = serializer.validated_data.get('sender')
                permitted_persons = Person.objects.filter(topics__name__in=request.data.get('topics'),
                                                          back_relations__trust_level__gte=request.data.get(
                                                              'min_trust_level'),
                                                          back_relations__person=sender)
                if len(permitted_persons) > 0:
                    received_persons_list = []
                    for permitted_person in permitted_persons:
                        Message.objects.create(text=serializer.validated_data.get('text'),
                                               sender=sender,
                                               recipient=permitted_person)
                        received_persons_list.append(permitted_person.name)

                        return JsonResponse({f'{sender.name}': received_persons_list}, status=HTTP_201_CREATED)
                return JsonResponse({'Message': "You don't have trusted friends by this topic :("},
                                    status=HTTP_200_OK)
            return JsonResponse({'Response': 400, 'Error': serializer.errors}, status=HTTP_400_BAD_REQUEST)
        return JsonResponse({'Response': 400, 'Error': 'All required arguments not provided'},
                            status=HTTP_400_BAD_REQUEST)


class PathView(APIView):
    def check(self, sender, request, i=1, result_list=[]):
        permitted_persons = Person.objects.filter(topics__name__in=request.data.get('topics'),
                                                  back_relations__trust_level__gte=request.data.get(
                                                      'min_trust_level'),
                                                  back_relations__person=sender)
        if len(permitted_persons) > 0:
            if len(result_list) > 0 and result_list[0][1] > i:
                result_list = [(permitted_persons, i)]
            elif len(result_list) == 0:
                result_list = [(permitted_persons, i)]
            return result_list
        else:
            trusted_persons = Person.objects.filter(back_relations__trust_level__gte=request.data.get(
                'min_trust_level'),
                back_relations__person=sender)
            for trusted_person in trusted_persons:
                checker = self.check(trusted_person, request, i=i+1, result_list=result_list)
                result_list = checker
            return result_list

    def post(self, request):
        if {'text', 'topics', 'from_person_id', 'min_trust_level'}.issubset(request.data):
            json_format = {"text": request.data.get('text'), "sender": request.data.get('from_person_id')}
            serializer = MessageSerializer(data=json_format)
            if serializer.is_valid():
                sender = serializer.validated_data.get('sender')
                recipients = self.check(sender, request)
                if len(recipients) > 0:
                    received_persons_list = []
                    for recipient in recipients[0][0]:
                        Message.objects.create(text=serializer.validated_data.get('text'),
                                               sender=sender,
                                               recipient=recipient)
                        received_persons_list.append(recipient.name)

                        return JsonResponse({"from": sender.name, "path": received_persons_list},
                                            status=HTTP_201_CREATED)
                else:
                    return JsonResponse({'Message': "No people by this topic :("},
                                        status=HTTP_200_OK)

            return JsonResponse({'Response': 400, 'Error': serializer.errors}, status=HTTP_400_BAD_REQUEST)
        return JsonResponse({'Response': 400, 'Error': 'All required arguments not provided'},
                            status=HTTP_400_BAD_REQUEST)
