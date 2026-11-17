# US-08: indexes for the question feed and keyword search.

from django.conf import settings
from django.db import migrations, models

# Django turns `title__icontains="x"` into
#   UPPER("questions_question"."title"::text) LIKE UPPER('%x%')
# on PostgreSQL. A B-tree cannot serve a leading-wildcard LIKE, but a pg_trgm GIN
# index on the *same expression* can. These are PostgreSQL-only, so they are
# skipped on SQLite (used by the local test suite).
TRIGRAM_INDEXES = {
    "question_title_trgm_idx": 'UPPER("title"::text)',
    "question_description_trgm_idx": 'UPPER("description"::text)',
}


def create_trigram_indexes(apps, schema_editor):
    if schema_editor.connection.vendor != "postgresql":
        return
    # pg_trgm is a "trusted" extension on PG13+, so the DB owner can create it.
    schema_editor.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")
    for name, expr in TRIGRAM_INDEXES.items():
        schema_editor.execute(
            f'CREATE INDEX IF NOT EXISTS "{name}" ON "questions_question" '
            f"USING gin (({expr}) gin_trgm_ops)"
        )


def drop_trigram_indexes(apps, schema_editor):
    if schema_editor.connection.vendor != "postgresql":
        return
    for name in TRIGRAM_INDEXES:
        schema_editor.execute(f'DROP INDEX IF EXISTS "{name}"')
    # The pg_trgm extension is left installed on purpose (harmless, may be shared).


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0004_analyticsevent_metadata_analyticsevent_session_id'),
        ('tags', '0002_tag_lookup_indexes'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddIndex(
            model_name='question',
            index=models.Index(condition=models.Q(('deleted_at__isnull', True)), fields=['-created_at', '-id'], name='question_live_created_idx'),
        ),
        migrations.AddIndex(
            model_name='question',
            index=models.Index(fields=['is_active', '-created_at'], name='question_active_created_idx'),
        ),
        migrations.RunPython(create_trigram_indexes, drop_trigram_indexes),
    ]
