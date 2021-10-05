import conversations
from django.db import models
from core import models as core_models


class Conversation(core_models.TimeSteampedModel):
    participants = models.ManyToManyField(
        "users.User", related_name="converstation", blank=True
    )

    def __str__(self):
        usernames = []
        for user in self.participants.all():
            # 위에 participants를 ManyToManyField 접근했으니
            # 여기서 안에 있는 유저들을 불러올 수 있음
            usernames.append(user.username)
        return ", ".join(usernames)
        # 당연하지만 __str__은 스트링만 반환하기 때문에 join을 사용하여 문자로 변환했다

    def count_messages(self):
        return self.messages.count()
        # conversations은 messages를 안가지고 있지만
        # messages에서 ForeignKey로 연결 했기 때문에 self.messages 가능

    def count_participants(self):
        return self.participants.count()

    count_messages.short_description = "메세지"
    count_participants.short_description = "대화 인원"


class Message(core_models.TimeSteampedModel):
    message = models.TextField()
    user = models.ForeignKey(
        "users.User", related_name="messages", on_delete=models.CASCADE
    )
    conversation = models.ForeignKey(
        "Conversation", related_name="messages", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user}님으로 부터 : {self.message}"
