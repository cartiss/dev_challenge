import json

from django.urls import reverse
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK
from rest_framework.test import APITestCase

from ..models import Person, Topic, TrustRelation, PersonTopic, Message


class ApiTestCase(APITestCase):

    def setUp(self):
        self.topic1, _ = Topic.objects.get_or_create(name='programming')
        self.topic2, _ = Topic.objects.get_or_create(name='movie')
        self.person1, _ = Person.objects.get_or_create(name='Test')
        self.person2, _ = Person.objects.get_or_create(name='Test2')
        self.person3, _ = Person.objects.get_or_create(name='Test3')
        self.person4, _ = Person.objects.get_or_create(name='Test4')
        self.person5, _ = Person.objects.get_or_create(name='Test5')
        self.person6, _ = Person.objects.get_or_create(name='Test6')
        self.person7, _ = Person.objects.get_or_create(name='Test7')
        self.topic_person, _ = PersonTopic.objects.get_or_create(person=self.person3, topic=self.topic1)
        self.topic_person2, _ = PersonTopic.objects.get_or_create(person=self.person4, topic=self.topic2)
        self.trust_relation, _ = TrustRelation.objects.get_or_create(person=self.person1, relation_person=self.person2,
                                                                     trust_level=9)
        self.trust_relatio2, _ = TrustRelation.objects.get_or_create(person=self.person1, relation_person=self.person7,
                                                                     trust_level=6)
        self.trust_relation3, _ = TrustRelation.objects.get_or_create(person=self.person1, relation_person=self.person4,
                                                                     trust_level=7)
        self.trust_relation4, _ = TrustRelation.objects.get_or_create(person=self.person2, relation_person=self.person3,
                                                                     trust_level=7)
        self.trust_relation5, _ = TrustRelation.objects.get_or_create(person=self.person4, relation_person=self.person5,
                                                                     trust_level=9)
        self.trust_relation6, _ = TrustRelation.objects.get_or_create(person=self.person5, relation_person=self.person6,
                                                                     trust_level=10)
        self.trust_relation7, _ = TrustRelation.objects.get_or_create(person=self.person6, relation_person=self.person3,
                                                                     trust_level=8)
        self.trust_relation8, _ = TrustRelation.objects.get_or_create(person=self.person7, relation_person=self.person5,
                                                                     trust_level=6)
        self.trust_relation9, _ = TrustRelation.objects.get_or_create(person=self.person7, relation_person=self.person2,
                                                                     trust_level=8)

    def test_create_person(self):
        url = reverse('people')
        data = {
            'name': 'Garry',
            'topics': ['books', 'magic']
        }
        data = json.dumps(data)
        response = self.client.post(url, data=data, content_type='application/json')
        person = Person.objects.all().last()
        self.assertEqual(response.json(), {'id': person.id, 'topics': ['books', 'magic']})
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_create_trust_connection(self):
        url = reverse('trust_connections', kwargs={'pk': self.person1.id})
        data = {
            '2': 10,
            '3': 5
        }
        data = json.dumps(data)
        response = self.client.post(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_update_trust_connection(self):
        url = reverse('trust_connections', kwargs={'pk': self.person1.id})
        data = {
            '2': 6,
        }
        data = json.dumps(data)
        response = self.client.post(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.trust_relation.refresh_from_db()
        self.assertEqual(self.trust_relation.trust_level, 6)

    def test_send_message(self):
        url = reverse('messages')
        data = {
            'text': 'Test text',
            'topics': ['movie'],
            'from_person_id': self.person1.id,
            'min_trust_level': 5
        }
        data = json.dumps(data)
        response = self.client.post(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.json(), {self.person1.name: ['Test4']})

    def test_send_message_low_trust_level_or_no_topics(self):
        url = reverse('messages')
        data = {
            'text': 'Test text',
            'topics': ['programming23'],
            'from_person_id': self.person1.id,
            'min_trust_level': 10
        }
        data = json.dumps(data)
        response = self.client.post(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.json(), {'Message': "You don't have trusted friends by this topic :("})

    def test_path(self):
        url = reverse('path')
        data = {
            'text': 'Test text',
            'topics': ['programming'],
            'from_person_id': self.person1.id,
            'min_trust_level': 5
        }
        data = json.dumps(data)
        response = self.client.post(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.json(), {"from": self.person1.name, "path": ['Test3']})
        messages = Message.objects.all()
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].text, 'Test text')
