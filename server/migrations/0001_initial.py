# Generated by Django 4.2.2 on 2023-06-22 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='user_registration',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_email', models.CharField(max_length=50)),
                ('user_password', models.CharField(max_length=16)),
            ],
        ),
    ]
