from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from vortraege.models import Talk
from textwrap import wrap

from django.template import Context, loader
from django.utils.safestring import mark_safe
from django.http import HttpResponse

from icalendar import Event
import base64
import StringIO
import qrcode
import qrcode.image.svg
import xml.etree.ElementTree
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
    description = '\n'.join(wrap(t.description, 80))
    response = render_to_response('vortraege/pressetext.txt', {'talk': t,
                                                               'start': t.start.strftime('%A, %d. %B %Y'),
                                                               'description': description})
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

    
def render_svg_aushang(talk):
    # The qrcode module tightly encapsulate its data.
    # blocking changes to the generated svg,
    # which is why we go he StringIO way.
    temp_out = StringIO.StringIO()
    qr = qrcode.QRCode()
    qr.add_data('http://www.youtube.com/watch?v=Y1g2Cx03L2I')
    img = qr.make_image(image_factory=qrcode.image.svg.SvgFragmentImage)
    img.save(temp_out)
    
    # Now change the XML so we can use it in the template
    e = xml.etree.ElementTree.fromstring(temp_out.getvalue())
    e.tag = '{http://www.w3.org/2000/svg}g'
    del e.attrib['version']
    # That should be inside the template.
    e.attrib['transform'] = 'translate(533.36055,279.81226)'

    # And finally render the poster
    template = loader.get_template('vortraege/aushang.svg')
    c = Context({'talk': talk,
                 'start': talk.start.strftime('%d.%m.%Y, %H:%M Uhr'),
                 'qrcode': mark_safe(xml.etree.ElementTree.tostring(e))})
    return template.render(c)    

def svg_aushang(request, talk_id):
    t = get_object_or_404(Talk, pk=talk_id)

    rendered = render_svg_aushang(t)

    response = HttpResponse(rendered)
    response['Content-Type'] = 'image/svg+xml; charset=utf-8'
    response['Content-Disposition']  = 'attachment; filename=aushang-%s.svg'%t.start.strftime('%Y%m')
    return response

def pdf_aushang(request, talk_id):
    t = get_object_or_404(Talk, pk=talk_id)

    rendered = render_svg_aushang(t)

    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition']  = 'attachment; filename=aushang-%s.pdf'%t.start.strftime('%Y%m')
    
    cairosvg.svg2pdf(bytestring=rendered.encode('utf-8'), write_to=response)

    return response

def svg_flyer(request, talk_id):
    v = get_object_or_404(Talk, pk=talk_id)
    header = wrap('%s: %s'%(v.speaker, v.title), 25)
    header1 = header[0]
    if len(header) > 1:
        header2 = header[1]
    else:
        header2 = u''
    response = render_to_response('vortraege/flyer.svg', {'talk': v,
                                                          'start': v.start.strftime('%d.%m.%Y, %H:%M Uhr'),
                                                          'header1': header1,
                                                          'header2': header2})
    response['Content-Type'] = 'image/svg+xml; charset=utf-8'
    response['Content-Disposition']  = 'attachment; filename=flyer-%s.svg'%v.start.strftime('%Y%m')
    return response

def pdf_flyer(request, talk_id):
    v = get_object_or_404(Talk, pk=talk_id)
    header = wrap('%s: %s'%(v.speaker, v.title), 25)
    header1 = header[0]
    if len(header) > 1:
        header2 = header[1]
    else:
        header2 = u''

    t = loader.get_template('vortraege/flyer.svg')
    c = Context({'talk': v,
                 'start': v.start.strftime('%d.%m.%Y, %H:%M Uhr'),
                 'header1': header1,
                 'header2': header2})
    rendered = t.render(c)

    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition']  = 'attachment; filename=flyer-%s.pdf'%v.start.strftime('%Y%m')
    
    cairosvg.svg2pdf(bytestring=rendered.encode('utf-8'), write_to=response)

    return response




