from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from rest_framework.decorators import api_view

from .models import Message
from .serializers import MessageSerializer
from rest_framework.response import Response
from .utils import format_quote, get_user_model, get_username_field

User = get_user_model()


@api_view(['GET'])
@login_required
def inbox(request):
    if request.method == 'GET':
        message_list = Message.objects.inbox_for(request.user)
        serializer = MessageSerializer(message_list, many = True)
    return Response(serializer.data)

@api_view(['GET'])
@login_required
def outbox(request):
    if request.method == 'GET':
        message_list = Message.objects.outbox_for(request.user)
        serializer = MessageSerializer(message_list, many = True)
    return Response(serializer.data)

@api_view(['GET'])
@login_required
def trash(request):
    if request.method == 'GET':
        message_list = Message.objects.trash_for(request.user)
        serializer = MessageSerializer(message_list, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@login_required
def compose(request, recipient=None, success_url=None, recipient_filter=None):
    if request.method == "POST":
        sender = request.user
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(sender=request.user)
            messages.info(request, _(u"Message successfully sent."))
            if success_url is None:
                success_url = reverse('messages_inbox')
            if 'next' in request.GET:
                success_url = request.GET['next']
            return Response(serializer.data), 
            HttpResponseRedirect(success_url)
    else:
        
        if recipient is not None:
            recipients = [u for u in User.objects.filter(**{'%s__in' % get_username_field(): [r.strip() for r in recipient.split('+')]})]
    return Response(serializer.data)

@api_view(['POST'])
@login_required
def reply(request, message_id, success_url=None,
        recipient_filter=None, quote_helper=format_quote,
        subject_template=_(u"Re: %(subject)s"),):
    """
    Prepares the ``form_class`` form for writing a reply to a given message
    (specified via ``message_id``). Uses the ``format_quote`` helper from
    ``messages.utils`` to pre-format the quote. To change the quote format
    assign a different ``quote_helper`` kwarg in your url-conf.
    """
    parent = get_object_or_404(Message, id=message_id)

    if parent.sender != request.user and parent.recipient != request.user:
        raise Http404

    if request.method == "POST":
        sender = request.user
        serializer = serializer(request.POST, recipient_filter=recipient_filter)
        if serializer.is_valid():
            serializer.save(sender=request.user, parent_msg=parent)
            messages.info(request, _(u"Message successfully sent."))
            if success_url is None:
                success_url = reverse('messages_inbox')
            return HttpResponseRedirect(success_url)
    else:
        form = form_class(initial={
            'body': quote_helper(parent.sender, parent.body),
            'subject': subject_template % {'subject': parent.subject},
            'recipient': [parent.sender,]
            })
    return Response(serializer.data)

@api_view(['GET','PUT','DELETE'])
def message_detail(request, message_id):
    try:
        message = Message.objects.get(message_id=message_id)
    except Message.DoesNotExit:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = 

@login_required
def delete(request, message_id, success_url=None):

    user = request.user
    now = timezone.now()
    message = get_object_or_404(Message, id=message_id)
    deleted = False
    if success_url is None:
        success_url = reverse('messages_inbox')
    if 'next' in request.GET:
        success_url = request.GET['next']
    if message.sender == user:
        message.sender_deleted_at = now
        deleted = True
    if message.recipient == user:
        message.recipient_deleted_at = now
        deleted = True
    if deleted:
        message.save()
        messages.info(request, _(u"Message successfully deleted."))
        if notification:
            notification.send([user], "messages_deleted", {'message': message,})
        return HttpResponseRedirect(success_url)
    raise Http404

@login_required
def undelete(request, message_id, success_url=None):
    """
    Recovers a message from trash. This is achieved by removing the
    ``(sender|recipient)_deleted_at`` from the model.
    """
    user = request.user
    message = get_object_or_404(Message, id=message_id)
    undeleted = False
    if success_url is None:
        success_url = reverse('messages_inbox')
    if 'next' in request.GET:
        success_url = request.GET['next']
    if message.sender == user:
        message.sender_deleted_at = None
        undeleted = True
    if message.recipient == user:
        message.recipient_deleted_at = None
        undeleted = True
    if undeleted:
        message.save()
        messages.info(request, _(u"Message successfully recovered."))
        if notification:
            notification.send([user], "messages_recovered", {'message': message,})
        return HttpResponseRedirect(success_url)
    raise Http404

@api_view(['GET'])
@login_required
def view(request, message_id):

    user = request.user
    now = timezone.now()
    message = get_object_or_404(Message, id=message_id)
    if (message.sender != user) and (message.recipient != user):
        raise Http404
    if message.read_at is None and message.recipient == user:
        message.read_at = now
        message.save()

    context = {'message': message, 'reply': None}
    if message.recipient == user:
        queryset = Message.objects.all()
        serializer = MessageSerializer(queryset, many=True)
    return Response(serializer.data)