# Generated by Django 4.1.7 on 2023-03-21 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_remove_user_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=200, null=True),
        ),
    ]