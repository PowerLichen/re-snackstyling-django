# Generated by Django 4.2 on 2023-04-24 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clothing_tag', '0001_initial'),
        ('clothing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='clothing',
            name='tags',
            field=models.ManyToManyField(to='clothing_tag.clothingtag'),
        ),
    ]
