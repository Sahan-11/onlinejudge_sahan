# Generated by Django 4.0.5 on 2022-07-07 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0002_rename_problems_problem_rename_testcases_testcase'),
    ]

    operations = [
        migrations.AddField(
            model_name='solution',
            name='sub_code',
            field=models.TextField(default='SOME STRING'),
        ),
    ]
