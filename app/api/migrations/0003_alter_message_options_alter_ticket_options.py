# Generated by Django 4.0.3 on 2022-03-19 19:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_message_ticket'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ('-id',)},
        ),
        migrations.AlterModelOptions(
            name='ticket',
            options={'ordering': ('-id',)},
        ),
    ]