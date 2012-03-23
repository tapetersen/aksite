# endcoding: utf-8

import ak
from django.db import models
from django.contrib.auth.models import User
from django.http import HttpResponse
import datetime

import logging
logger = logging.getLogger(__name__)

class MailVerificationSent(models.Model):
    email = models.CharField(max_length=128)
    sent = models.DateTimeField(auto_now_add=True)
    
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def mailsender(request):
    
    mail = request.FILES[u"file"].read()
    to = request.GET["to"]
    
    #split headers
    i = mail.find("\n\n")
    headers, mail = mail[:i], mail[i:]
    headers = headers.split("\n")
    allowed = {"MIME-Version", "Message-ID", "In-Reply-To", "Content-Type", 
               "Date", "Subject", "From", "To", "Bcc", "Cc", "References"}
    
    from_ = None
    
    h = []
    i=0
    while i<len(headers):
        add = False
        header = headers[i][:headers[i].find(":")]
        if header in allowed:
            add = True
        if header == "From":
            from_ = headers[i][headers[i].find(":")+1:].strip()
            
        while True:
            if add: 
                h.append(headers[i])
            i += 1
            if i>=len(headers) or headers[i][0] not in " \t":
                break
            
    mail = "\n".join(h) + mail
    
    #find from email
    i = from_.find("<")
    if i != -1:
        from_ = from_[i+1:]
        from_ = from_[:from_.find(">")]
    
    #logger.info("headers: %s", str(headers))
    #logger.info("h: %s", str(h))
    
    logger.info("Mail from %s to %s recieved", from_, to)
    # Only allow sending from altekamereren domains and registered users.
    if not from_.endswith("@altekamereren.org") \
            and not from_.endswith("@altekamereren.com") \
            and User.objects.filter(email=from_).exists():
        logger.info("Sender not accepted.")
        return HttpResponse(status=403)
    
    to = to.replace(u"flojt", u"flöjt")
    reciever = to.split("@")[0]
    if reciever in ak.sections:
        user_emails = [user.email for user in User.objects.filter(
            instrument__in=ak.section_to_short_instruments[reciever], 
            is_active=True)]

        

        logger.info("Sending to section %s: %s", to, str(user_emails))

    elif reciever == u"infolistan":
        reciever = [user.email for user in User.objects.filter(is_active=True)]
        logger.info("Sending to infolistan: %s", str(reciever))
    else:
        logger.info("List not accepted.")
        return HttpResponse(status=400)
    
    from django.conf import settings
    from boto.ses import SESConnection
    from boto.exception import BotoServerError
    
    access_key_id = getattr(settings, 'AWS_ACCESS_KEY_ID', None)
    access_key = getattr(settings, 'AWS_SECRET_ACCESS_KEY', None)
    api_endpoint = getattr(settings, 'AWS_SES_API_HOST',
                                     SESConnection.DefaultHost)
    connection = SESConnection(
                aws_access_key_id=access_key_id,
                aws_secret_access_key=access_key,
                host=api_endpoint,
    )
    
    if not user_emails:
        return HttpResponse(status=400)

    try:
        connection.send_raw_email(mail, settings.ADMINS[0][1], user_emails)
    except BotoServerError as e:
        i = e.body.find("<Message>")
        message = e.body[i+len("<Message>"):]
        message = message[:message.find("</Message>")]
        
        if message == "Email address is not verified.":
            if MailVerificationSent.objects.filter(email=from_, 
                    sent__gte=datetime.datetime.now() - datetime.timedelta(days=1)
                        ).exists():
                connection.verify_email_address(from_)
                logger.error("Sending verify mail to: %s", from_)
                MailVerificationSent(email=from_).save()
            else:
                logger.error("Verify mail already sent today: %s", from_)
            return HttpResponse(status=444)
        else:
            raise

    
    return HttpResponse()
