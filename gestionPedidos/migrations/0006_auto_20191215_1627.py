# Generated by Django 2.2.7 on 2019-12-15 15:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestionPedidos', '0005_auto_20191215_1623'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='treatment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='gestionPedidos.Tratamiento'),
        ),
    ]