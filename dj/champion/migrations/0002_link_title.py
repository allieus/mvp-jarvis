# Generated by Django 3.0.9 on 2020-08-20 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('champion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='title',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
