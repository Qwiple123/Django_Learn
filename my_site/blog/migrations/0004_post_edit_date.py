# Generated by Django 4.1.7 on 2023-03-12 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_comment_delete_commit'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='edit_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
