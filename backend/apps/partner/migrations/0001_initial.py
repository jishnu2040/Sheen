# Generated by Django 5.0.4 on 2024-07-10 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='PartnerDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_name', models.CharField(max_length=200)),
                ('website', models.URLField(blank=True, null=True)),
                ('team_size', models.IntegerField()),
                ('location', models.CharField(max_length=255)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('service_type', models.ManyToManyField(related_name='partners', to='partner.servicetype')),
            ],
        ),
    ]
