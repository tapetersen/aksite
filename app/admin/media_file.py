import datetime
import logging
from django.core.urlresolvers import reverse
from django.forms import ComboField
from django.utils import six
from django.utils.html import escape
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from feincms.content.medialibrary.models import MediaFileContentInline
from feincms.module.medialibrary.fields import MediaFileForeignKeyRawIdWidget
from feincms.module.medialibrary.forms import MediaFileAdminForm
from feincms.module.medialibrary.modeladmins import MediaFileAdmin
from feincms.module.medialibrary.models import Category, MediaFile, MediaFileTranslation, MediaFileBase
from django.http import HttpResponseRedirect
from django.conf import settings

from django.utils.translation import ugettext_lazy as _
from feincms.module.medialibrary.thumbnail import admin_thumbnail
from feincms.utils import shorten_string


@staticmethod
@csrf_protect
@permission_required('medialibrary.add_mediafile')
def bulk_upload(request):
    from django.core.urlresolvers import reverse
    from os import path

    if request.method == 'POST' and 'data' in request.FILES:

        category = None
        if request.POST.get('category'):
            category = Category.objects.get(pk=int(request.POST.get('category')))
            
        from django.template.defaultfilters import slugify
        from django.core.files.base import ContentFile
        
        for uploaded_file in request.FILES.getlist('data'):
            fname, ext = path.splitext(uploaded_file.name)
            target_fname = slugify(fname) + ext.lower()
            
            mf = MediaFile()
            mf.file.save(target_fname, uploaded_file)
            mf.save()
    
            if category:
                mf.categories.add(category)
    
            mt = MediaFileTranslation()
            mt.parent  = mf
            mt.caption = fname.replace('_', ' ')
            mt.save()

        messages.info(request, _("%d files imported") % len(request.FILES.getlist('data')))
    else:
        messages.error(request, _("No input file given"))
            
    return HttpResponseRedirect(reverse('admin:medialibrary_mediafile_changelist'))
MediaFileAdmin.bulk_upload = bulk_upload

MediaFileContentInline.radio_fields = {}

def label_for_value(self, value):
    key = self.rel.get_related_field().name
    try:
        obj = self.rel.to._default_manager.using(self.db).get(
            **{key: value})
        label = ['&nbsp;<strong>%s</strong>' % escape(
            shorten_string(six.text_type(obj)))]
        image = admin_thumbnail(obj)

        label.append(' <a href="{0}" target="_blank">preview</a>'.format(obj.file.url))
        url = reverse('admin:{0}_{1}_change'.format(obj._meta.app_label, obj._meta.module_name), args=(obj.pk,))
        label.append(' <a href="{0}" target="_blank">edit</a>'.format(url))



        if image:
            label.append(
                '<br /><img src="%s" alt="" style="margin:1em 0 0 10em"'
                '/>' % image)

        return ''.join(label)
    except (ValueError, self.rel.to.DoesNotExist):
        return ''
MediaFileForeignKeyRawIdWidget.label_for_value = label_for_value

def save(self, *args, **kwargs):
    if not self.id and not self.created:
        self.created = datetime.now()

    self.type = self.determine_file_type(self.file.name)
    if self.file:
        try:
            self.file_size = self.file.size
        except (OSError, IOError, ValueError) as e:
            logging.error("Unable to read file size for %s: %s", self, e)

    if getattr(self, '_original_file_name', None):
        if self.file.name != self._original_file_name:
            self.file.storage.delete(self._original_file_name)

    super(MediaFileBase, self).save(*args, **kwargs)
    self.purge_translation_cache()
MediaFileBase.save = save

class Media:
    js = (settings.JQUERY_URL,
          #"js/libs/jquery.html5_upload.js",
          "js/upload.js")
    
MediaFileAdmin.Media = Media
