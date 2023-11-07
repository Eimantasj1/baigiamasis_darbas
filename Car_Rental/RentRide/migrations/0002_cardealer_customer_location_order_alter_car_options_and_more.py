# Generated by Django 4.2.5 on 2023-11-07 12:04

import RentRide.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('RentRide', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarDealer',
            fields=[
                ('car_dealer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('phone', models.CharField(max_length=10, validators=[django.core.validators.MinLengthValidator(10), django.core.validators.MaxLengthValidator(10)])),
                ('earnings', models.IntegerField(default=0)),
                ('type', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('phone', models.CharField(max_length=10, validators=[django.core.validators.MinLengthValidator(10), django.core.validators.MaxLengthValidator(10)])),
                ('type', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('city', models.CharField(max_length=50, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rent', models.CharField(max_length=10)),
                ('days', models.PositiveSmallIntegerField()),
                ('is_complete', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.AlterModelOptions(
            name='car',
            options={},
        ),
        migrations.RenameField(
            model_name='car',
            old_name='year',
            new_name='capacity',
        ),
        migrations.RenameField(
            model_name='car',
            old_name='model',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='car',
            name='brand',
        ),
        migrations.RemoveField(
            model_name='car',
            name='car_image',
        ),
        migrations.RemoveField(
            model_name='car',
            name='notes',
        ),
        migrations.RemoveField(
            model_name='car',
            name='price_per_day',
        ),
        migrations.AddField(
            model_name='car',
            name='image',
            field=models.ImageField(default=1, upload_to='car_images/', validators=[RentRide.models.validate_car_image]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='car',
            name='rent',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.DeleteModel(
            name='Rental',
        ),
        migrations.AddField(
            model_name='order',
            name='car',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RentRide.car'),
        ),
        migrations.AddField(
            model_name='order',
            name='car_dealer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RentRide.cardealer'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='customer',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RentRide.location'),
        ),
        migrations.AddField(
            model_name='cardealer',
            name='location',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='RentRide.location'),
        ),
        migrations.AddField(
            model_name='car',
            name='car_dealer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='RentRide.cardealer'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='car',
            name='location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='RentRide.location'),
        ),
    ]