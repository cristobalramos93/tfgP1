# Generated by Django 2.2.7 on 2019-12-12 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionPedidos', '0003_auto_20191212_2135'),
    ]

    operations = [
        migrations.AddField(
            model_name='centro_medico',
            name='postal',
            field=models.IntegerField(blank=True, max_length=250, null=True),
        ),
    ]
