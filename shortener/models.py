from django.db import models
import random
import string

def generate_short_url():
    characters = string.ascii_letters + string.digits
    shorter_url = ''.join(random.choice(characters) for _ in range(6))
    return shorter_url

class URL(models.Model):
    original_url = models.URLField()
    shorter_url = models.CharField(max_length=10, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.shorter_url