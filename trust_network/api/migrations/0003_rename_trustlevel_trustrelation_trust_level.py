# Generated by Django 4.1.1 on 2022-09-29 19:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_person_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trustrelation',
            old_name='trustLevel',
            new_name='trust_level',
        ),
    ]
