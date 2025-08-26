from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("market", "0001_initial"),  # replace with the last migration in your market app
    ]

    operations = [
        migrations.RenameField(
            model_name="product",
            old_name="owner",
            new_name="farmer",
        ),
    ]
