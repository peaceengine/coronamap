# Generated by Django 3.0.4 on 2020-03-23 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statements', '0012_auto_20200323_1036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statement',
            name='icon',
            field=models.ImageField(default='static/statements/opinion_choice.png', upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='statement',
            name='iconAgree',
            field=models.ImageField(default='static/statements/agree.png', upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='statement',
            name='iconDisagree',
            field=models.ImageField(default='static/statements/disagree.png', upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='statement',
            name='image',
            field=models.ImageField(default='static/statements/opinion_choice.png', upload_to='images/'),
        ),
    ]
