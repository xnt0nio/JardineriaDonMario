# Generated by Django 3.1.2 on 2023-06-22 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_historialcompra'),
    ]

    operations = [
        migrations.AddField(
            model_name='historialcompra',
            name='cantidad',
            field=models.IntegerField(default=0),
        ),
    ]
