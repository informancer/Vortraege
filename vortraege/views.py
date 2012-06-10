from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from vortraege.models import Talk
from textwrap import wrap

from django.template import Context, loader
from django.http import HttpResponse
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.detail import BaseDetailView
from django.views.generic import TemplateView

from icalendar import Event
import cairosvg

class AttachmentResponseMixin(TemplateResponseMixin):
    content_type = None
    filename_prefix = None

    def render_to_response(self, context, **response_kwargs):
        if self.content_type is None:
            raise ImproperlyConfigured(
                "AttachmentResponseMixin requires a definition of 'content_type'")
        response = super(AttachmentResponseMixin, self).render_to_response(context, 
                                                                          **response_kwargs)
        
        response['Content-Type'] = self.content_type
        response['Content-Disposition']  = 'attachment; filename=%s'%self.get_filename(context)
        return response

    def get_filename(self, context):
        if self.filename_prefix is None:
            raise ImproperlyConfigured(
                "AttachmentResponseMixin requires a definition of 'filename_prefix'")
        return '%s-%s.txt'%(self.filename_prefix,
                            context['object'].start.strftime('%Y%m'))

# Create your views here.
class PlainTextDetailView(AttachmentResponseMixin, BaseDetailView):
    pass

def vevent(request, talk_id):
    t = get_object_or_404(Talk, pk=talk_id)
    event = Event()
    event.add('description', t.title)
    ical = event.to_ical
    response = HttpResponse(ical, mimetype='text/calendar')
    response['Filename'] = 'filename.ics'  # IE needs this
    response['Content-Disposition'] = 'attachment; filename=talk-%s.ics'%t.start.strftime('%Y%m')
    return response

    
def render_svg_poster(talk):

    template = loader.get_template('vortraege/aushang.svg')
    c = Context({'talk': talk})
    return template.render(c)    

def svg_poster(request, talk_id):
    t = get_object_or_404(Talk, pk=talk_id)

    rendered = render_svg_poster(t)

    response = HttpResponse(rendered)
    response['Content-Type'] = 'image/svg+xml; charset=utf-8'
    response['Content-Disposition']  = 'attachment; filename=aushang-%s.svg'%t.start.strftime('%Y%m')
    return response

def pdf_poster(request, talk_id):
    t = get_object_or_404(Talk, pk=talk_id)

    rendered = render_svg_poster(t)

    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition']  = 'attachment; filename=aushang-%s.pdf'%t.start.strftime('%Y%m')
    
    cairosvg.svg2pdf(bytestring=rendered.encode('utf-8'), write_to=response)

    return response

def render_svg_flyer(talk):
    template = loader.get_template('vortraege/flyer.svg')
    c = Context({'talk': talk})
    return template.render(c)    
    

def svg_flyer(request, talk_id):
    talk = get_object_or_404(Talk, pk=talk_id)

    rendered = render_svg_flyer(talk)

    response = HttpResponse(rendered)
    response['Content-Type'] = 'image/svg+xml; charset=utf-8'
    response['Content-Disposition']  = 'attachment; filename=flyer-%s.svg'%talk.start.strftime('%Y%m')
    return response

def pdf_flyer(request, talk_id):
    talk = get_object_or_404(Talk, pk=talk_id)

    rendered = render_svg_flyer(talk)

    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition']  = 'attachment; filename=flyer-%s.pdf'%talk.start.strftime('%Y%m')
    
    cairosvg.svg2pdf(bytestring=rendered.encode('utf-8'), write_to=response)

    return response



