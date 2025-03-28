# Generated by Django 4.2.7 on 2025-03-24 18:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('airport_backend', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='flight',
            name='airplane',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flight', to='airport_backend.airplane'),
        ),
        migrations.AddField(
            model_name='flight',
            name='crew',
            field=models.ManyToManyField(related_name='flights', to='airport_backend.crew'),
        ),
        migrations.AddField(
            model_name='flight',
            name='route',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flight', to='airport_backend.route'),
        ),
        migrations.AddField(
            model_name='airplane',
            name='airplane_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='airplane', to='airport_backend.airplanetype'),
        ),
    ]
