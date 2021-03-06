from django.core.management.base import BaseCommand

from user.models import UserProfile


class Command(BaseCommand):
    def handle(self, *args, **options):
        username = 'root'
        email = 'root@vj.com'
        password = 'rootroot'
        if UserProfile.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING('Due to the existence of this user, no new user was created'))
        else:
            user = UserProfile.objects.create_superuser(username=username, email=email, password=password)
            user.save()
