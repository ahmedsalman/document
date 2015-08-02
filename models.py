from south.modelsinspector import add_ignored_fields
add_ignored_fields(["^taggit\.managers"])

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _

from taggit.managers import TaggableManager


class TimeStampAwareModel( models.Model ):
    """
    A model class that can be used as super class
    for any model that is considered timestamp aware 
    model.
    """
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_deleted = models.DateTimeField(blank=True, null=True)

    def is_deleted(self):
        if self.date_deleted:
            return True
        return False
    is_deleted.boolean = True
    
    class Meta:
        abstract = True


class Document( TimeStampAwareModel ):
    """
    Document model
    """
    DOCUMENT_TYPE_CHOICES = (
        ('', ''),
        ('AR', 'Article'),
        ('BK', 'Book'),
        ('CH', 'Chapter'),
        ('CP', 'Conference Proceeding'),
        ('PA', 'Patent'),
        ('TH', 'Thesis'),
        ('DS', 'Dataset'),
    )

    author = models.ForeignKey(User)

    document = models.FileField(_('document'), upload_to = 'documents/')
    title = models.CharField(_('title'), max_length = 150)
    abstract = models.CharField(_('abstract'), max_length = 1000, blank = True, null = True)
    description = models.TextField(_('description'), blank = True, null = True)
    doc_type = models.CharField(_('document type'), max_length = 2, blank = True, null = True, choices = DOCUMENT_TYPE_CHOICES)
    date_published = models.DateField(_('date published'), blank = True, null = True)

    tags = TaggableManager()

    def __unicode__(self):
        return _("%s") % (self.title)

    class Meta:
        app_label = "document"
        verbose_name = "document"
        verbose_name_plural = "documents"


class CoAuthor( TimeStampAwareModel ):
    """
    CoAuthor Model
    """
    userprofile = models.ForeignKey(User, blank = True, null = True)
    document =  models.ForeignKey(Document, related_name="%(app_label)s_%(class)s_related")
    
    name = models.CharField(_('name'), max_length = 100, blank = True, null = True)

    def __unicode__(self):
        if self.userprofile:
            return _("%s_%s") % (self.document.title, self.userprofile.get_full_name())
        else:
            return _("%s_%s") % (self.document.title, self.name)

    class Meta:
        verbose_name = "co-author"
        verbose_name_plural = "co-authors"
