# Generated by Django 5.0.6 on 2024-05-18 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0004_rename_usefulls_habit_usefull'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habit',
            name='reward',
            field=models.CharField(max_length=100, null=True, verbose_name='Вознагрождение'),
        ),
    ]
