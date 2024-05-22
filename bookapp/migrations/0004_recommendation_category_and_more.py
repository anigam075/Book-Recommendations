# Generated by Django 5.0.6 on 2024-05-22 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookapp', '0003_recommendation_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='recommendation',
            name='category',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='recommendation',
            name='publication_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='recommendation',
            name='rating',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
