# Generated by Django 5.0.7 on 2024-09-16 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kvm', '0007_xmldata_xml_hash'),
    ]

    operations = [
        migrations.AlterField(
            model_name='xmldata',
            name='xml_hash',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
