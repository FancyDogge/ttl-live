# Generated by Django 4.0.2 on 2022-02-27 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, max_length=300, null=True)),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('DEADLINE', 'Deadline soon'), ('PAUSED', 'Paused'), ('DONE', 'Done')], default='ACTIVE', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
