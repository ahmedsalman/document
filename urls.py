from django.conf.urls.defaults import patterns, include, url

from document.views import delete_document, my_documents_list, document, download_document, upload_document


urlpatterns = patterns('', 

    url(r'^(?P<doc_id>[-\d]+)/$',
       document,
       {'template_name': 'document/document.html'},
       name = 'document'
    ),

    url(r'^(?P<username>[-\w\.]+)/documents-list/$',
       my_documents_list,
       {'template_name': 'document/my_document.html'},
       name = 'my_documents_list'
    ),

    url(r'^download/(?P<doc_id>[-\d]+)/$',
       download_document,
       name = 'download_document'
    ),

    url(r'^upload/$',
       upload_document,
       name = 'upload_document'
    ),
    

    url(r'^user/delete/document/(?P<doc_id>[-\d]+)/$',
       delete_document,
       name = 'delete_document'
    ),
    
)
