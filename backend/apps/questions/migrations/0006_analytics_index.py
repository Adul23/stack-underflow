from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("questions", "0005_search_indexes")]
    operations = [migrations.AddIndex(
        model_name="analyticsevent",
        index=models.Index(fields=["event_name", "created_at"], name="event_type_created_idx"),
    )]
