# Generated by Django 4.0.3 on 2022-05-05 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Game', '0004_rename_player_1_status_gamelobby_gamefinished_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameinvite',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]