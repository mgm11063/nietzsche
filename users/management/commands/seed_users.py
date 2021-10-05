from django.core.management.base import BaseCommand
from django_seed import Seed
from users.models import User


# seed 작업 말 그대로 씨앗을 뿌리는 작업이랑 똑같음
# 페이크 db를 만드는데 하나하나 우리가 선택해서 만들기 귀찮으니까
# seed for를 통해서 추가하는 작업


class Command(BaseCommand):
    help = "This command creates amenities"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=2, type=int, help="How many users you want to create"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        seeder.add_entity(User, number, {"is_staff": False, "is_superuser": False})
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} users created!"))
