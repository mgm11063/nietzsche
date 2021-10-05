import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from rooms import models as room_models
from users import models as user_models


class Command(BaseCommand):

    help = "This command creates amenities"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=2, type=int, help="How many rooms you want to create"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        all_users = user_models.User.objects.all()
        room_types = room_models.RoomType.objects.all()
        seeder.add_entity(
            room_models.Room,
            number,
            {
                "name": lambda x: seeder.faker.address(),
                "host": lambda x: random.choice(all_users),
                "room_type": lambda x: random.choice(room_types),
                "gusests": lambda x: random.randint(1, 20),
                "price": lambda x: random.randint(1, 300),
                "beds": lambda x: random.randint(1, 5),
                "bedrooms": lambda x: random.randint(1, 5),
                "baths": lambda x: random.randint(1, 5),
            },
        )
        created_photos = seeder.execute()
        # 씨드로 포토를 뿌림
        created_clean = flatten(list(created_photos.values()))
        # 그냥 포토의 아이디 값을 깔끔하게 만든작업
        amenities = room_models.Amenity.objects.all()
        facilities = room_models.Facility.objects.all()
        rules = room_models.HouseRule.objects.all()
        for pk in created_clean:
            room = room_models.Room.objects.get(pk=pk)
            # 룸에 아이디를 가져옴
            for i in range(3, random.randint(10, 30)):
                # 최소 3개의 이미지와 최대 10~17개 사이로 렌덤하게 생성함
                room_models.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    # caption(설명)은 페이커에서 그냥 아무말이나 가져옴
                    file=f"room_photos/{random.randint(1, 15)}.webp",
                    #
                    room=room,
                    # 당연히 룸은 위에서 생성한 룸
                )
            for a in amenities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.amenities.add(a)
            for f in facilities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.facilities.add(f)
            for r in rules:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.house_rules.add(r)
            # 렌덤으로 짝수 것들을 추가함
        self.stdout.write(self.style.SUCCESS(f"{number}개의 방을 생성하였습니다!"))
