# Generated by Django 4.1.1 on 2022-09-29 23:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trustrelation',
            name='relation_person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='back_relations', to='api.person'),
        ),
    ]
