# Generated by Django 4.2.5 on 2023-11-10 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('display', '0004_club_approved'),
        ('blog', '0003_post_club'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThingsToApprove',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clubs', models.ManyToManyField(to='display.club')),
                ('posts', models.ManyToManyField(to='blog.post')),
            ],
        ),
    ]
