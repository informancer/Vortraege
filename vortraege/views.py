from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from vortraege.models import Talk
from textwrap import wrap

from django.template import Context, loader
from django.http import HttpResponse

from icalendar import Event
import cairosvg

# Create your views here.
def index(request): 
    talks_list = Talk.objects.all().order_by('start')
    return render_to_response('vortraege/index.html', 
                              {
            'talks_list': talks_list,
            })
    return HttpResponse(t.render(c))

def details(request, talk_id):
    t = get_object_or_404(Talk, pk=talk_id)
    return render_to_response('vortraege/details.html', {'talk': t})

def pressetext(request, talk_id):
    t = get_object_or_404(Talk, pk=talk_id)
    response = render_to_response('vortraege/pressetext.txt', {'talk': t})
    response['Content-Type'] = 'text/plain; charset=utf-8'
    response['Content-Disposition']  = 'attachment; filename=pressetext-%s.txt'%t.start.strftime('%Y%m')
    return response

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




