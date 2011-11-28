# endcoding: utf8

import ak
from django.db import models
from django.contrib.auth.models import User
import datetime

import logging

class MailVerificationSent(models.Model):
    email = models.CharField(max_length=128)
    sent = models.DateTimeField(auto_now_add=True)
    
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def mailsender(request):
    from django.http import HttpResponse
    
    mail = request.FILES[u"file"].read()
    to = request.GET["to"]
    
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
        print i
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
    
    i = from_.find("<")
    if i != -1:
        from_ = from_[i+1:]
        from_ = from_[:from_.find(">")]
    
    #logging.info("headers: %s", str(headers))
    #logging.info("h: %s", str(h))
    
    logging.info("Mail from %s to %s recieved", from_, to)
    if not from_.endswith("@altekamereren.org") \
            and not from_.endswith("@altekamereren.com") \
            and User.objects.filter(email=from_).count() < 1:
        logging.info("Sender not accepted.")
        return HttpResponse(status=400)
    
    if to == u"flojt":
        to = u"flöjt"
    
    if to in ak.sections:
        to = [user.email for user in User.objects.filter(
            instrument__in=ak.section_to_short_instruments[to], 
            is_active=True)]
        
        logging.info("Sending to section: %s", str(to))
    elif to == u"infolistan":
        to = [user.email for user in User.objects.filter(is_active=True)]
        logging.info("Sending to infolistan: %s", str(to))
    else:
        logging.info("List not accepted.")
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
    
    try:
        connection.send_raw_email(mail, "sam@bostream.nu", to)
    except BotoServerError as e:
        i = e.body.find("<Message>")
        message = e.body[i+len("<Message>"):]
        message = message[:message.find("</Message>")]
        
        if message == "Email address is not verified.":
            if MailVerificationSent.objects.filter(email=from_, 
                    sent__gte=datetime.datetime.now() - datetime.timedelta(days=1)
                        ).count() < 1:
                connection.verify_email_address(from_)
                logging.error("Sending verify mail to: %s", from_)
                MailVerificationSent(email=from_).save()
            else:
                logging.error("Verify mail already sent today: %s", from_)
            return HttpResponse(status=444)
        else:
            raise
    
    return HttpResponse()