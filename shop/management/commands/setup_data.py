"""Setup initial categories and sample products."""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from shop.models import Category, Product

User = get_user_model()


class Command(BaseCommand):
    help = "Add initial categories and sample data"

    def handle(self, *args, **options):
        categories_data = [
            ("arduino", "Arduino", "Arduino boards and shields"),
            ("raspberry-pi", "Raspberry Pi", "Raspberry Pi boards and accessories"),
            ("sensors", "Sensors", "Temperature, humidity, motion sensors"),
            ("actuators", "Actuators", "Servos, stepper motors, relays"),
            ("motors", "Motors", "DC motors, stepper motors"),
        ]
        for slug, name, desc in categories_data:
            cat, _ = Category.objects.get_or_create(slug=slug, defaults={"name": name, "description": desc})
            self.stdout.write(f"Category: {cat.name}")

        # Create seller and sample product if none exist
        if not Product.objects.exists():
            seller = User.objects.filter(role="seller").first()
            if not seller:
                seller = User.objects.create_user("seller1", "seller@roboshop.com", "seller123", role="seller")
            cat = Category.objects.first()
            if cat:
                Product.objects.get_or_create(
                    slug="arduino-uno",
                    defaults={
                        "name": "Arduino Uno R3",
                        "category": cat,
                        "description": "Classic Arduino Uno board for electronics projects.",
                        "price": 25.99,
                        "stock": 50,
                        "seller": seller,
                    }
                )
                self.stdout.write(self.style.SUCCESS("Sample product created."))
