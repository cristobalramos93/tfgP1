# Generated by Django 2.2.7 on 2019-11-21 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Articulos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
                ('seccion', models.CharField(max_length=30)),
                ('precio', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Clientes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
                ('direccion', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('telefono', models.CharField(max_length=7)),
            ],
        ),
        migrations.CreateModel(
            name='Pedidos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.IntegerField()),
                ('fecha', models.DateField()),
                ('entregado', models.BooleanField()),
            ],
        ),
    ]
