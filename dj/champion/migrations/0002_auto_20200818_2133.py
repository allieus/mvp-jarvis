# Generated by Django 3.0.9 on 2020-08-18 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('champion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='label',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='link',
            name='mvp_tag',
            field=models.CharField(db_index=True, help_text='ex) AI-MVP-1234567', max_length=20),
        ),
    ]
