# Generated by Django 3.0.4 on 2020-03-22 11:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('statements', '0003_auto_20200322_1114'),
    ]

    operations = [
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_text', models.CharField(max_length=200)),
                ('votes', models.IntegerField(default=0)),
                ('statement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='statements.Statement')),
            ],
        ),
    ]
