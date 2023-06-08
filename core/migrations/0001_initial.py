# Generated by Django 3.1.2 on 2023-05-03 02:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TipoProducto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('precio', models.IntegerField()),
                ('stock', models.IntegerField()),
                ('descripcion', models.CharField(max_length=250)),
                ('vencimiento', models.DateField()),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='')),
                ('vigente', models.BooleanField()),
                ('tipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.tipoproducto')),
            ],
        ),
    ]