from django.contrib import admin
from django.utils.html import mark_safe
from . import models


@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):
    """Item Admin Definition"""

    list_display = ("name", "used_by")

    def used_by(self, obj):
        return obj.rooms.count()

    pass


class PhtoInline(admin.TabularInline):
    # TabularInline
    # 룸 어드민에서 포토어드민에서 사진추가 하는 기능을 가져 옴
    # 장고가 ForeignKey 랑 연결된 유저 룸을 자동적으로 찾아서 가능함
    model = models.Photo


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    """Room Admin Definition"""

    # def save_model(self, obj, form, change):
    #     return super().save_model( obj, form, change)

    # 어드민에서 저장하는 것을 담당함 모델에서 def save와는 약간 다름
    # 리퀘스트로 어떤 유저가 요청했는 지 등 다양한 걸 알수 있음
    # 오브젝트, html , 변수 True or Flase 반환
    # 어드민에서만 변수가 적용됨

    inlines = (PhtoInline,)

    fieldsets = (
        (
            "기본정보",
            {"fields": ("name", "description", "country", "city", "address", "price")},
        ),
        ("시간", {"fields": ("check_in", "check_out", "instant_book")}),
        ("방", {"fields": ("gusests", "beds", "bedrooms", "baths")}),
        (
            "방에 대한 세부 정보",
            {
                "classes": ("collapse",),  # 접을 수 있는 섹션으로 만듬
                "fields": ("amenities", "facilities", "house_rules"),
            },
        ),
        ("세부정보", {"fields": ("host",)}),
    )

    ordering = ("name", "price", "bedrooms")

    list_display = (
        "name",
        "country",
        "city",
        "price",
        "gusests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        # 여기부턴 many to many 는 함수로 불러와야함
        "count_amenities",
        "count_photos",
        "total_rating",
    )

    list_filter = (
        "instant_book",
        "host__superhost",  # line num "43" 참조
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
        "city",
        "country",
    )

    raw_id_fields = ("host",)
    # 유저가 많은데 긴 리스트로 선택하는 방법을 가지고 싶지 않을때 사용한다

    search_fields = ("=city", "^host__username")
    # = ^ 연산자는 그냥 검색 설정
    # host 뒤에 붙는 __##는 ForeignKey에 접근하는 것과 똑같음

    filter_horizontal = ("amenities", "facilities", "house_rules")

    def count_amenities(self, obj):
        return obj.amenities.count()

    def count_photos(self, obj):
        return obj.photos.count()

    # 지금 모델에서 별개 클레스인데 끌고올 수 있는 이유
    # 모델에 phtos class 에서  ForeignKey 로 Room class가 연결되어있음
    # 그래서 똑똑이 리스트 때문에 옵젝의 데이터를 가지고 올수있음
    count_photos.short_description = "사진 겟수"


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """Photo Admin Definition"""

    list_display = ("__str__", "get_thumbnail")

    def get_thumbnail(self, obj):
        return mark_safe(f'<img width="35px" src = "{obj.file.url}"/>')
        # photo의 오브젝트를 이용해서 url을 가져왔다
        # 인풋에 스크립트가 들어가면 해킹의 문제가 발생하기때문에
        # mark_safe를 사용하여 괜찮은 str이라고 설정해 줬다

    get_thumbnail.short_description = "썸네일"
