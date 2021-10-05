from django.core.management.base import BaseCommand
from rooms import models as room_models


# seed 작업 말 그대로 씨앗을 뿌리는 작업이랑 똑같음
# 페이크 db를 만드는데 하나하나 우리가 선택해서 만들기 귀찮으니까
# seed for를 통해서 추가하는 작업


class Command(BaseCommand):
    help = "amenities를 만드는 커맨드 입니다 :)"

    """ def add_arguments(self, parser):
        parser.add_argument("--times", help="아 아무거나 적어") """

    def handle(self, *args, **options):
        amenities = [
            "Air conditioning",
            "Alarm Clock",
            "Balcony",
            "Bathroom",
            "Bathtub",
            "Bed Linen",
            "Boating",
            "Cable TV",
            "Carbon monoxide detectors",
            "Chairs",
            "Children Area",
            "Coffee Maker in Room",
            "Cooking hob",
            "Cookware & Kitchen Utensils",
            "Dishwasher",
            "Double bed",
            "En suite bathroom",
            "Free Parking",
            "Free Wireless Internet",
            "Freezer",
            "Fridge / Freezer",
            "Golf",
            "Hair Dryer",
            "Heating",
            "Hot tub",
            "Indoor Pool",
            "Ironing Board",
            "Microwave",
            "Outdoor Pool",
            "Outdoor Tennis",
            "Oven",
            "Queen size bed",
            "Restaurant",
            "Shopping Mall",
            "Shower",
            "Smoke detectors",
            "Sofa",
            "Stereo",
            "Swimming pool",
            "Toilet",
            "Towels",
            "TV",
        ]
        for a in amenities:
            if not room_models.Amenity.objects.filter(name=a):
                room_models.Amenity.objects.create(name=a)
            self.stdout.write(self.style.SUCCESS("Amenities created!"))
