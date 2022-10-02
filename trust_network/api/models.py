from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Topic(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Person(models.Model):
    name = models.CharField(max_length=100, unique=True)
    topics = models.ManyToManyField('Topic', related_name='persons', through='PersonTopic')
    relations = models.ManyToManyField("self", through='TrustRelation')


class PersonTopic(models.Model):
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    topic = models.ForeignKey('Topic', on_delete=models.CASCADE)


class TrustRelation(models.Model):
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    relation_person = models.ForeignKey('Person', on_delete=models.CASCADE, related_name="back_relations")
    trust_level = models.IntegerField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1),
        ]
    )


class Message(models.Model):
    text = models.CharField(max_length=400)
    sender = models.ForeignKey('Person', on_delete=models.CASCADE, related_name="sent_messages")
    recipient = models.ForeignKey('Person', related_name="received_messages", on_delete=models.CASCADE)
