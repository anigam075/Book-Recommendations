# Generated by Django 5.0.6 on 2024-05-22 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookapp', '0002_remove_recommendation_rating_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='recommendation',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]
