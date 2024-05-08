# Generated by Django 5.0.4 on 2024-05-08 08:00

import core.models
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('contact_details', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('user_type', models.CharField(choices=[('customer', 'Customer'), ('vendor', 'Vendor')], max_length=20)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('vendor_code', models.CharField(default=core.models.generate_vendor_code, max_length=6, primary_key=True, serialize=False)),
                ('contact_details', models.TextField()),
                ('address', models.TextField()),
                ('name', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('po_number', models.CharField(default=core.models.generate_vendor_code, max_length=6, primary_key=True, serialize=False)),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('delivery_date', models.DateTimeField()),
                ('items', models.JSONField()),
                ('quantity', models.IntegerField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('informed', 'Informed'), ('listed', 'Listed'), ('completed', 'Completed'), ('canceled', 'Canceled')], default='pending', max_length=20)),
                ('quality_rating', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0, 'Rating cannot be negative')])),
                ('issue_date', models.DateTimeField(blank=True, null=True)),
                ('acknowledgment_date', models.DateTimeField(blank=True, null=True)),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.vendor')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalPerformance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('on_time_delivery_rate', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0, 'Rate cannot be negative')])),
                ('quality_rating_avg', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0, 'Rating cannot be negative')])),
                ('average_response_time', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0, 'Time cannot be negative')])),
                ('fulfillment_rate', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0, 'Rate cannot be negative')])),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.vendor')),
            ],
        ),
    ]
