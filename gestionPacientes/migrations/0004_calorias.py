# Generated by Django 2.2.8 on 2019-12-28 16:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestionPacientes', '0003_auto_20191227_1346'),
    ]

    operations = [
        migrations.CreateModel(
            name='Calorias',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('calories', models.FloatField(max_length=250)),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gestionPacientes.Paciente')),
            ],
            options={
                'db_table': 'calorias',
                'unique_together': {('id_user', 'time')},
            },
        ),
    ]
