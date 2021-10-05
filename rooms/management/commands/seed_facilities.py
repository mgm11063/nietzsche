from django.core.management.base import BaseCommand
from rooms import models as room_models


# seed 작업 말 그대로 씨앗을 뿌리는 작업이랑 똑같음
# 페이크 db를 만드는데 하나하나 우리가 선택해서 만들기 귀찮으니까
# seed for를 통해서 추가하는 작업


class Command(BaseCommand):
    help = "facilities 만드는 커맨드 입니다 :)"

    """ def add_arguments(self, parser):
        parser.add_argument("--times", help="아 아무거나 적어") """

    def handle(self, *args, **options):
        facilities = [
            "Private entrance",
            "Paid parking on premises",
            "Paid parking off premises",
            "Elevator",
            "Parking",
            "Gym",
        ]
        for f in facilities:
            if not room_models.Amenity.objects.filter(name=f):
                room_models.Facility.objects.create(name=f)
        self.stdout.write(
            self.style.SUCCESS(f"{len(facilities)}개의 facilities가 생성되었습니다.")
        )
