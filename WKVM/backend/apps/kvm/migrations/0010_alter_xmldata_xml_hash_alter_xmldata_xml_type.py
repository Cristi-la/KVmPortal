# Generated by Django 5.0.7 on 2024-09-23 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kvm', '0009_vm_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='xmldata',
            name='xml_hash',
            field=models.CharField(blank=True, help_text='SHA-256 hash of the XML data. Leave blank to auto-calculate.', max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='xmldata',
            name='xml_type',
            field=models.CharField(choices=[('CAPABILITIES', 'Domain capabilities'), ('SMBIOS', 'System Management BIOS (SMBIOS)'), ('OTHER', 'Other XML data')], default='OTHER', max_length=50),
        ),
    ]
