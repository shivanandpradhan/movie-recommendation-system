# Generated by Django 4.0.4 on 2022-06-24 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0002_collabarativemovierecommender'),
    ]

    operations = [
        migrations.AddField(
            model_name='collabarativemovierecommender',
            name='movie6',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]