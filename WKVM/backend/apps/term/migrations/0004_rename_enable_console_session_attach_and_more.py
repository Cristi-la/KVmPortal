# Generated by Django 5.0.7 on 2024-08-01 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('term', '0003_session_enable_console_session_save_output_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='session',
            old_name='enable_console',
            new_name='attach',
        ),
        migrations.RenameField(
            model_name='session',
            old_name='save_output',
            new_name='saveoutput',
        ),
        migrations.AddField(
            model_name='session',
            name='reaonly',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='session',
            name='status',
            field=models.CharField(choices=[('init', 'Init'), ('running', 'Running'), ('closed', 'Closed'), ('completed', 'Completed'), ('failed', 'Failed')], default='init', max_length=255),
        ),
    ]