# Generated by Django 5.0.4 on 2024-04-25 09:37

import django.contrib.auth.models
import django.db.models.deletion
import django.utils.timezone
import embed_video.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=400)),
                ('k', models.CharField(default='1', max_length=400)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=400)),
                ('k', models.CharField(default='1', max_length=400)),
            ],
        ),
        migrations.CreateModel(
            name='Year',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=400)),
                ('k', models.CharField(default='1', max_length=400)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('name', models.CharField(max_length=200, null=True)),
                ('username', models.CharField(max_length=200, null=True)),
                ('email', models.EmailField(max_length=254, null=True, unique=True)),
                ('year', models.CharField(max_length=200, null=True)),
                ('gov', models.CharField(max_length=200, null=True)),
                ('prov', models.CharField(max_length=200, null=True)),
                ('school', models.CharField(max_length=200, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='LessonEval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.PositiveSmallIntegerField(default=0)),
                ('total', models.PositiveSmallIntegerField(default=0)),
                ('percent', models.PositiveSmallIntegerField(default=0)),
                ('k', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.lesson')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Outcome',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=400)),
                ('content', models.TextField()),
                ('img', models.ImageField(default=False, upload_to='')),
                ('video', embed_video.fields.EmbedVideoField(default=False)),
                ('k', models.CharField(default='1', max_length=400)),
                ('p', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.lesson')),
                ('y', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.year')),
            ],
        ),
        migrations.CreateModel(
            name='OutcomeEval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.PositiveSmallIntegerField(default=0)),
                ('total', models.PositiveSmallIntegerField(default=0)),
                ('percent', models.PositiveSmallIntegerField(default=0)),
                ('k', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.outcome')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(null=True)),
                ('op1', models.CharField(max_length=200, null=True)),
                ('op2', models.CharField(max_length=200, null=True)),
                ('op3', models.CharField(max_length=200, null=True)),
                ('op4', models.CharField(max_length=200, null=True)),
                ('hint', models.TextField(null=True)),
                ('level', models.CharField(max_length=400, null=True)),
                ('img', models.ImageField(default=False, upload_to='')),
                ('video', embed_video.fields.EmbedVideoField(default=False)),
                ('k', models.CharField(default='1', max_length=400)),
                ('l', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.lesson')),
                ('p', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.outcome')),
                ('s', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.subject')),
            ],
        ),
        migrations.CreateModel(
            name='QEval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.SmallIntegerField(default=0)),
                ('flag', models.PositiveSmallIntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('k', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.question')),
            ],
        ),
        migrations.CreateModel(
            name='QDubl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(null=True)),
                ('op1', models.CharField(max_length=200, null=True)),
                ('op2', models.CharField(max_length=200, null=True)),
                ('op3', models.CharField(max_length=200, null=True)),
                ('op4', models.CharField(max_length=200, null=True)),
                ('hint', models.TextField(null=True)),
                ('level', models.CharField(max_length=400, null=True)),
                ('img', models.ImageField(default=False, upload_to='')),
                ('video', embed_video.fields.EmbedVideoField(default=False)),
                ('k', models.CharField(default='1', max_length=400)),
                ('p', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.question')),
            ],
        ),
        migrations.CreateModel(
            name='SubjectEval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.PositiveSmallIntegerField(default=0)),
                ('total', models.PositiveSmallIntegerField(default=0)),
                ('percent', models.PositiveSmallIntegerField(default=0)),
                ('k', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.subject')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=400)),
                ('k', models.CharField(default='1', max_length=400)),
                ('p', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.subject')),
                ('y', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.year')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='u',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.unit'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='p',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.unit'),
        ),
        migrations.CreateModel(
            name='UnitEval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.PositiveSmallIntegerField(default=0)),
                ('total', models.PositiveSmallIntegerField(default=0)),
                ('percent', models.PositiveSmallIntegerField(default=0)),
                ('k', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.unit')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='subject',
            name='p',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.year'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='y',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.year'),
        ),
        migrations.CreateModel(
            name='YearEval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percent', models.PositiveSmallIntegerField(default=0)),
                ('k', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.year')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
