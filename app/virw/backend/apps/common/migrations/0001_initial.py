# Generated by Django 5.0.7 on 2024-10-17 23:54

import django.contrib.auth.validators
import django.db.models.deletion
import django_tenants.postgresql_backend.base
import tenant_users.permissions.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TenantUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(db_index=True, max_length=254, unique=True, verbose_name='Email Address')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('is_verified', models.BooleanField(default=False, help_text='Designates whether this user has verified their email address.', verbose_name='verified')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=(models.Model, tenant_users.permissions.models.PermissionsMixinFacade),
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schema_name', models.CharField(db_index=True, max_length=63, unique=True, validators=[django_tenants.postgresql_backend.base._check_schema_name])),
                ('slug', models.SlugField(blank=True, verbose_name='Tenant URL Name')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('type', models.CharField(choices=[('private', 'Private'), ('global', 'Global')], default='global', max_length=100)),
                ('enabled_until', models.DateField(blank=True, null=True)),
                ('is_trial', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('on_maintenance', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='tenantuser',
            name='tenants',
            field=models.ManyToManyField(blank=True, help_text='The tenants this user belongs to.', related_name='user_set', to='common.client', verbose_name='tenants'),
        ),
        migrations.CreateModel(
            name='ClientDomain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(db_index=True, max_length=253, unique=True)),
                ('is_primary', models.BooleanField(db_index=True, default=True)),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='domains', to='common.client')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
