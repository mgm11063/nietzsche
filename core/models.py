from django.db import models


class TimeSteampedModel(models.Model):

    """Time Stamped Model"""

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # 오브젝트 생성시 그 오브젝트의 데이터와 시간 등을 장고가 보여주도록 저장함

    class Meta:
        abstract = True

    # 메타 클레스로 데이터 베이스로 가는 걸 막음
