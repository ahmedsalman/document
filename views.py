import unicodedata

from django.contrib.sites.models import Site
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

from document.models import CoAuthor, Document
from document.forms import DocumentUploadForm

from django.db.models import Q
from annoying.decorators import ajax_request

def document(request, doc_id, template_name):
    """
    Document page
    """
    
    try:
        notifications = request.user.notifications.unread()
    except AttributeError:
        notifications = ""
    
    try:
        document = Document.objects.get(id = doc_id)
    except Document.DoesNotExist:
        messages.error(request, "Document does not exist.")
        return HttpResponseRedirect(reverse('homepage'))

    try:
        user = document.author
    except:
        messages.error(request, "User does not exist.")
        return HttpResponseRedirect(reverse('homepage'))

    try:
        profile = document.author.get_profile()
    except:
        messages.error(request, "Profile does not exist.")
        return HttpResponseRedirect(reverse('homepage'))

    coauthors = CoAuthor.objects.filter(document = document)

    related_doc_widget = Document.objects.filter( Q(tags__in = profile.tags.all()) , date_deleted = None).order_by('?')
    if not related_doc_widget:
        related_doc_widget = Document.objects.filter( date_deleted = None).order_by("?")

    no_of_documents = len( Document.objects.filter(author = user) )

    context = {
        'coauthors': coauthors,
        'document': document,
        'related_doc_widget': related_doc_widget,
        'user': user,
        'profile':profile,
        'no_of_documents':no_of_documents,
        'notifications': notifications,
        'site': Site.objects.get_current(),
    }

    return render_to_response(template_name, context, context_instance=RequestContext(request))


def my_documents_list(request, username, template_name , page_template):
    """
    my documents list
    """
    
    try:
        notifications = request.user.notifications.unread()
    except AttributeError:
        notifications = ""
    
    try:
        user_profile = User.objects.get(username = username)
    except User.DoesNotExist:
        messages.error(request, "Not a valid profile name.")
        return HttpResponseRedirect(reverse('homepage'))
    
    documents = Document.objects.filter( author = user ).order_by("-date_added")
    followers_widget = Felloz.objects.get_followers(user = user_profile)
    followings_widget = Felloz.objects.get_followings(user = user_profile)
    no_of_documents = len( Document.objects.filter(author = user) )

    context = {
        'documents': documents, 
        'page_template': page_template,
        'followers_widget': followers_widget,
        'followings_widget': followings_widget,
        'related_doc_widget': related_doc_widget,
        'profile':user_profile,
        'no_of_documents':no_of_documents,
        'notifications': notifications,
    }

    if request.is_ajax():
        template_name = page_template
    return render_to_response(template_name, context, context_instance=RequestContext(request))

    return render_to_response(template_name, context, context_instance=RequestContext(request))


def download_document(request, doc_id):
    """
    Download a document
    """
    try:
        document = Document.objects.get(id = doc_id)
    except Document.DoesNotExist:
        messages.error(request, "Document does not exist.")
        return HttpResponseRedirect('/')

    filename = document.document.name.split('/')[-1]

    ext = ['.doc' ,'.dot' ,'.docx' ,'.dotx' ,'.docm' ,'.dotm' ,'.xls' ,'.xlt' ,'.xla' ,'.xlsx' ,'.xltx' ,'.xlsm' ,'.xltm' 
    ,'.xlam' ,'.xlsb' ,'.ppt' ,'.pot' ,'.pps' ,'.ppa' ,'.pptx' ,'.potx' ,'.ppsx' ,'.ppam' ,'.pptm' ,'.potm' ,'.ppsm', '.pdf']

    mime_type = ['application/msword' 
    ,'application/msword'
    ,'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    ,'application/vnd.openxmlformats-officedocument.wordprocessingml.template'
    ,'application/vnd.ms-word.document.macroEnabled.12'
    ,'application/vnd.ms-word.template.macroEnabled.12'
    ,'application/vnd.ms-excel'
    ,'application/vnd.ms-excel'
    ,'application/vnd.ms-excel'
    ,'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    ,'application/vnd.openxmlformats-officedocument.spreadsheetml.template'
    ,'application/vnd.ms-excel.sheet.macroEnabled.12'
    ,'application/vnd.ms-excel.template.macroEnabled.12'
    ,'application/vnd.ms-excel.addin.macroEnabled.12'
    ,'application/vnd.ms-excel.sheet.binary.macroEnabled.12'
    ,'application/vnd.ms-powerpoint'
    ,'application/vnd.ms-powerpoint'
    ,'application/vnd.ms-powerpoint'
    ,'application/vnd.ms-powerpoint'
    ,'application/vnd.openxmlformats-officedocument.presentationml.presentation'
    ,'application/vnd.openxmlformats-officedocument.presentationml.template'
    ,'application/vnd.openxmlformats-officedocument.presentationml.slideshow'
    ,'application/vnd.ms-powerpoint.addin.macroEnabled.12'
    ,'application/vnd.ms-powerpoint.presentation.macroEnabled.12'
    ,'application/vnd.ms-powerpoint.presentation.macroEnabled.12'
    ,'application/vnd.ms-powerpoint.slideshow.macroEnabled.12'
    ,'application/pdf']


    for x ,y in zip( ext, mime_type ):
        if filename.endswith(x):
            response = HttpResponse(document.document, mimetype=y)
            response['Content-Disposition'] = 'attachment; filename=%s' % filename

            return response

    response = HttpResponse(document.document, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    
    return response


@csrf_protect
@login_required
def upload_document(request): 
    """
    Upload a document
    """
    page = request.GET.get('next', '')

    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES, user = request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Document uploaded.")
            docs = Document.objects.filter(author = request.user)
            
            user_profile = request.user
        if page:
            return HttpResponseRedirect(reverse(page))
        return HttpResponseRedirect(reverse('my_documents_list', args=[request.user.username]))
    else:
        messages.error(request, "Something went wrong!")
        if page:
            return HttpResponseRedirect(reverse(page))
        return HttpResponseRedirect(reverse('my_documents_list', args=[request.user.username]))


@csrf_protect
@login_required
def delete_document(request, doc_id):
    """
    delete document
    """
    if request.method == "POST":
        try:
            document = Document.objects.get(id = doc_id , author = request.user)
            document.delete()
            messages.error(request, "successfully deleted the document.")
            return HttpResponseRedirect(reverse('homepage'))
        except Document.DoesNotExist:
            messages.error(request, "Document does not exist.")
            return HttpResponseRedirect(reverse('homepage'))
        messages.error(request, "Invalid request.")
        return HttpResponseRedirect(reverse('homepage'))


