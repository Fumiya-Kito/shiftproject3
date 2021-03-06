# Generated by Django 3.0.7 on 2020-06-19 15:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('1', 'フロント'), ('2', 'ショップ'), ('3', 'ボックス'), ('4', 'コンセ'), ('5', '映写'), ('6', '早朝清掃')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('name', models.CharField(max_length=50)),
                ('gender', models.CharField(choices=[('1', '男性'), ('2', '女性'), ('3', 'その他')], default='1', max_length=1)),
                ('duties', models.CharField(choices=[('1', 'リーダー'), ('2', 'ベテラン'), ('3', '新人')], default='3', max_length=1)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('section', models.ManyToManyField(to='account.Section', verbose_name='セクション')),
            ],
        ),
    ]
