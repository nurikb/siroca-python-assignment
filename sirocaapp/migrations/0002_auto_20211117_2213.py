# Generated by Django 3.2.9 on 2021-11-17 16:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sirocaapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='userrequest',
            table='UserRequest',
        ),
        migrations.AlterModelTable(
            name='userrequestresult',
            table='UserRequestResult',
        ),
    ]
