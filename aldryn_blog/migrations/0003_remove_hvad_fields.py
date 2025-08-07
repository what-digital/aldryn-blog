# Generated migration to remove hvad fields and complete parler transition

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aldryn_blog', '0002_auto_20200409_1202'),
    ]

    operations = [
        # Remove the hvad-specific _hvad_query field that was added in 0002
        migrations.RemoveField(
            model_name='category',
            name='_hvad_query',
        ),
        # Update the CategoryTranslation model to remove hvad-specific master field
        # and ensure it's compatible with parler
        migrations.AlterModelManagers(
            name='category',
            managers=[
                ('objects', 'parler.managers.TranslatableManager()'),
            ],
        ),
    ]
