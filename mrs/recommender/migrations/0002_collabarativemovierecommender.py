# Generated by Django 4.0.4 on 2022-06-24 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CollabarativeMovieRecommender',
            fields=[
                ('userId', models.IntegerField(primary_key=True, serialize=False)),
                ('movie1', models.IntegerField()),
                ('movie2', models.IntegerField()),
                ('movie3', models.IntegerField()),
                ('movie4', models.IntegerField()),
                ('movie5', models.IntegerField()),
            ],
        ),
    ]
