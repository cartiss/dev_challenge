from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Topic(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Person(models.Model):
    name = models.CharField(max_length=100, unique=True)
    topics = models.ManyToManyField('Topic', related_name='persons', through='PersonTopic')
    relations = models.ManyToManyField('Person', through='TrustRelation')


class PersonTopic(models.Model):
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    topic = models.ForeignKey('Topic', on_delete=models.CASCADE)


class TrustRelation(models.Model):
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    relation_person = models.ForeignKey('Person', on_delete=models.CASCADE, related_name='relation_person')
    trustLevel = models.IntegerField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1),
        ]
    )
