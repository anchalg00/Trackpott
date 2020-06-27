from datetime import datetime
from datetime import timedelta  
from django.conf import settings
from django.core.mail import send_mail
from materials.models import Requirement

from django.utils import timezone


def run():
	for requirement in Requirement.objects.all():
		if(  requirement.time_due - timedelta(hours=24) <= datetime.now(tz=timezone.utc)): 
			subject="Due date is in 2 days"
			message = "welcome "
			from_email = settings.EMAIL_HOST_USER
			to_list = [settings.EMAIL_HOST_USER]
			send_mail(subject,message,from_email,to_list)
			print(requirement.spool_details)
		

# for requirement in Requirement.objects.filter(time_due = datetime.today(tz=timezone.utc) + timedelta(days=2)):