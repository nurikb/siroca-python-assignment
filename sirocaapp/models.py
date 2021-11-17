from django.db import models


class UserRequest(models.Model):
    url = models.CharField(max_length=150, db_index=True, unique=True)

    def __str__(self):
        return '{}'.format(self.url)

    class Meta:
        db_table = "UserRequest"


class UserRequestResult(models.Model):
    url = models.ForeignKey(UserRequest, on_delete=models.CASCADE)
    pull_name = models.CharField(max_length=150, db_index=True, null=True)
    reviewers_name = models.CharField(max_length=150, db_index=True)
    assignees_name = models.CharField(max_length=150, db_index=True)
    pull_url = models.CharField(max_length=150, db_index=True)

    class Meta:
        db_table = "UserRequestResult"
