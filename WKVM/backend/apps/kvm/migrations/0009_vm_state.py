# Generated by Django 5.0.7 on 2024-09-20 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kvm', '0008_alter_xmldata_xml_hash'),
    ]

    operations = [
        migrations.AddField(
            model_name='vm',
            name='state',
            field=models.CharField(choices=[('running', 'Running'), ('idle', 'Idle'), ('paused', 'Paused'), ('in shutdown', 'In Shutdown'), ('shut off', 'Shut Off'), ('crashed', 'Crashed'), ('pm suspended', 'PM Suspended'), ('no info', 'No Info')], default='no info', max_length=50),
        ),
    ]