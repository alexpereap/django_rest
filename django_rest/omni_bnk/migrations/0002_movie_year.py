# Generated by Django 2.2 on 2019-04-03 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('omni_bnk', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='year',
            field=models.CharField(default=None, max_length=20),
            preserve_default=False,
        ),
    ]