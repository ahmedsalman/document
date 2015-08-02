import re
from django import forms
from django.contrib.auth.models import User

from document.models import CoAuthor, Document


class DocumentUploadForm( forms.Form ):
    """
    Document Upload Form
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

    coauthor = forms.CharField(max_length = 100, required=False)
    document_tags = forms.CharField(max_length = 1000, required=False)
    document = forms.FileField()
    title = forms.CharField(max_length = 150)
    abstract = forms.CharField(max_length = 1000, required=False)
    description =  forms.CharField(widget = forms.Textarea, required=False)
    doc_type = forms.ChoiceField(widget = forms.Select(), 
                     choices = DOCUMENT_TYPE_CHOICES, required=False)
    date_published = forms.DateField(required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(DocumentUploadForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(DocumentUploadForm, self).clean()
        return cleaned_data

    def save(self, *args, **kwargs):
        title = self.cleaned_data['title']
        document = self.cleaned_data['document']
        abstract = self.cleaned_data['abstract']
#        description = self.cleaned_data['description']
        doc_type = self.cleaned_data['doc_type']
        coauthors = self.cleaned_data['coauthor']
        document_tags = self.cleaned_data['document_tags']
        date_published = self.cleaned_data['date_published']

        try:
            author = User.objects.get(username = self.user)
        except User.DoesNotExist:
            return None
 
        document = Document(
                            title = title, 
                            document = document, 
#                            description = description,
                            description = abstract,
                            abstract = abstract, 
                            author = author,
                            date_published = date_published,
                            doc_type = doc_type
                            )
        document.save()

#        junkers = re.compile('[[" \]]')
#        result = junkers.sub('', document_tags).split(',')

#        document_tags = '"'.join(document_tags)
#        document_tags = '['.join(document_tags)
#        document_tags = ']'.join(document_tags)
        result = document_tags.split(',')


        if result:
            for tag in result:
                document.tags.add( tag );
#        document.tags.add( document_tags );

        if coauthors:
            coauthors = coauthors.split(',')
            for coauthor in coauthors:
                obj = CoAuthor(document = document, name = coauthor)
                obj.save()
        return document
