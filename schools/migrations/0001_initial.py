# Generated by Django 4.2.4 on 2023-09-13 03:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='The official name of the university in full', max_length=250, unique=True)),
                ('nickname', models.CharField(blank=True, help_text='The short unofficial names or abbreviation the university is known as e.g. eksu, adopoly, unilag', max_length=100, null=True, unique=True)),
                ('slug', models.SlugField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='The official name of the faulty', max_length=250)),
                ('nickname', models.CharField(blank=True, help_text='The short unofficial name of the faculty if any', max_length=100, null=True)),
                ('university', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='faculties', to='schools.university')),
            ],
            options={
                'verbose_name_plural': 'faculties',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='The official name of the department', max_length=250)),
                ('nickname', models.CharField(blank=True, help_text='The short unofficial name of the department if any', max_length=100, null=True, unique=True)),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departments', to='schools.faculty')),
            ],
        ),
        migrations.CreateModel(
            name='Association',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='aid')),
                ('name', models.CharField(max_length=250, verbose_name='association name')),
                ('academic_session', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('association_history', models.JSONField(default=dict, help_text='store information about past association and the president information')),
                ('constituency_name', models.CharField(blank=True, max_length=128, null=True, verbose_name='constituency name')),
                ('department', models.ForeignKey(help_text='Department should only be provided if the association is a department association', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='associations', to='schools.department')),
                ('faculty', models.ForeignKey(help_text='Faculty should only be provided if the association is a faculty association', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='associations', to='schools.faculty')),
                ('general_secretary', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='general_secretary_of', to=settings.AUTH_USER_MODEL)),
                ('president', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='president_of', to=settings.AUTH_USER_MODEL)),
                ('treasurer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='treasurer_of', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='faculty',
            constraint=models.UniqueConstraint(fields=('university', 'name'), name='unique_faculties'),
        ),
        migrations.AddConstraint(
            model_name='department',
            constraint=models.UniqueConstraint(fields=('faculty', 'name'), name='unique_departments'),
        ),
    ]