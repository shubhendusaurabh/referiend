import time
from sys import stdout

from django.conf import settings
from django.core.management.base import CommandError, NoArgsCommand

from django.contrib.auth.models import User
from django.core.mail import send_mail

class Command(NoArgsCommand):

    help = "Send out email to everyone"

    def handle(self, *args, **options):
        print >> stdout, "Commencing big email send"

        users = User.objects.all()

        for index, user in enumerate(users):
            if not user.email.strip():
                continue
            send_mail(
                    subject=settings.BIG_EMAIL_SEND_SUBJECT,
                    message=settings.BIG_EMAIL_SEND,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email,],
            )
            print 'Sent to', index, user.email
            time.sleep(1)
