# Generated by Django 3.0.8 on 2020-08-18 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('keywords', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('company', models.CharField(max_length=50)),
                ('address', models.CharField(blank=True, max_length=100)),
                ('phone', models.CharField(blank=True, max_length=15)),
                ('fax', models.CharField(blank=True, max_length=15)),
                ('email', models.CharField(blank=True, max_length=50)),
                ('smptserver', models.CharField(blank=True, max_length=20)),
                ('smptemail', models.CharField(blank=True, max_length=20)),
                ('smptpassword', models.CharField(blank=True, max_length=10)),
                ('smptport', models.CharField(blank=True, max_length=5)),
                ('icon', models.ImageField(blank=True, upload_to='Images/')),
                ('facebook', models.CharField(blank=True, max_length=50)),
                ('instagram', models.CharField(blank=True, max_length=50)),
                ('twitter', models.CharField(blank=True, max_length=50)),
                ('aboutus', models.TextField(blank=True)),
                ('contact', models.TextField(blank=True)),
                ('references', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('False', 'Hayır'), ('True', 'Evet')], max_length=10)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
