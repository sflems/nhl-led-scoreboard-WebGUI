# Generated by Django 3.1.3 on 2021-05-16 18:57

from django.db import migrations, models
import scoreboard.services


class Migration(migrations.Migration):

    dependencies = [
        ('scoreboard', '0005_auto_20210516_1117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boardtype',
            name='board',
            field=models.CharField(choices=[('Scoreboards', (('mlb', 'MLB'), ('nfl', 'NFL'), ('nhl', 'NHL'))), ('Custom', ())], default='nhl', max_length=16, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='settings',
            name='config',
            field=models.JSONField(blank=True, default=scoreboard.services.conf_default, null=True),
        ),
    ]
