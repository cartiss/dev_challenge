# Generated by Django 4.1.1 on 2022-09-29 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='name',
            field=models.CharField(default='Test', max_length=100, unique=True),
            preserve_default=False,
        ),
    ]