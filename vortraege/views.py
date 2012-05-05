from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from vortraege.models import Vortrag
from textwrap import wrap

from django.template import Context, loader
from django.http import HttpResponse

from icalendar import Event
import StringIO
import base64
import qrcode
import qrcode.image.svg
import cairosvg

# Create your views here.
def index(request): 
    vortraege_list = Vortrag.objects.all().order_by('datum')
    return render_to_response('vortraege/index.html', 
                              {
            'vortraege_list': vortraege_list,
            })
    return HttpResponse(t.render(c))

def details(request, vortrag_id):
    v = get_object_or_404(Vortrag, pk=vortrag_id)
    return render_to_response('vortraege/details.html', {'vortrag': v})

def pressetext(request, vortrag_id):
    v = get_object_or_404(Vortrag, pk=vortrag_id)
    beschreibung = '\n'.join(wrap(v.beschreibung, 80))
    response = render_to_response('vortraege/pressetext.txt', {'vortrag': v,
                                                               'datum': v.datum.strftime('%A, %d. %B %Y'),
                                                               'beschreibung': beschreibung})
    response['Content-Type'] = 'text/plain; charset=utf-8'
    response['Content-Disposition']  = 'attachment; filename=pressetext-%s.txt'%v.datum.strftime('%Y%m')
    return response

def vevent(request, vortrag_id):
    v = get_object_or_404(Vortrag, pk=vortrag_id)
    event = Event()
    event.add('description', v.thema)
    ical = event.to_ical
    response = HttpResponse(ical, mimetype='text/calendar')
    response['Filename'] = 'filename.ics'  # IE needs this
    response['Content-Disposition'] = 'attachment; filename=vortrag-%s.ics'%v.datum.strftime('%Y%m')
    return response

def pdf_aushang(request, vortrag_id):
    v = get_object_or_404(Vortrag, pk=vortrag_id)

    temp_out = StringIO.StringIO()
    img = qrcode.make('http://www.youtube.com/watch?v=Y1g2Cx03L2I')
    img.save(temp_out)
    encoded = base64.b64encode(temp_out.getvalue())

    t = loader.get_template('vortraege/aushang.svg')
    c = Context({'vortrag': v,
                 'datum': v.datum.strftime('%d.%m.%Y, %H:%M Uhr'),
                 'termin': encoded})
    rendered =  t.render(c)

    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition']  = 'attachment; filename=aushang-%s.pdf'%v.datum.strftime('%Y%m')
    
    cairosvg.svg2pdf(bytestring=rendered.encode('utf-8'), write_to=response)

    return response
    
def svg_aushang(request, vortrag_id):
    v = get_object_or_404(Vortrag, pk=vortrag_id)

    temp_out = StringIO.StringIO()
    img = qrcode.make('http://www.youtube.com/watch?v=Y1g2Cx03L2I')
    img.save(temp_out)
    encoded = base64.b64encode(temp_out.getvalue())

    t = loader.get_template('vortraege/aushang.svg')
    c = Context({'vortrag': v,
                 'datum': v.datum.strftime('%d.%m.%Y, %H:%M Uhr'),
                 'termin': encoded})
    rendered = t.render(c)

    response = HttpResponse(rendered)
    response['Content-Type'] = 'image/svg+xml; charset=utf-8'
    response['Content-Disposition']  = 'attachment; filename=aushang-%s.svg'%v.datum.strftime('%Y%m')
    return response

def pdf_flyer(request, vortrag_id):
    v = get_object_or_404(Vortrag, pk=vortrag_id)
    header = wrap('%s: %s'%(v.referent, v.thema), 25)
    header1 = header[0]
    if len(header) > 1:
        header2 = header[1]
    else:
        header2 = u''

    t = loader.get_template('vortraege/flyer.svg')
    c = Context({'vortrag': v,
                 'datum': v.datum.strftime('%d.%m.%Y, %H:%M Uhr'),
                 'header1': header1,
                 'header2': header2,
                 'termin': encoded})
    rendered = t.render(c)

    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition']  = 'attachment; filename=flyer-%s.pdf'%v.datum.strftime('%Y%m')
    
    cairosvg.svg2pdf(bytestring=rendered.encode('utf-8'), write_to=response)

    return response

def svg_flyer(request, vortrag_id):
    v = get_object_or_404(Vortrag, pk=vortrag_id)
    header = wrap('%s: %s'%(v.referent, v.thema), 25)
    header1 = header[0]
    if len(header) > 1:
        header2 = header[1]
    else:
        header2 = u''
    response = render_to_response('vortraege/flyer.svg', {'vortrag': v,
                                                          'datum': v.datum.strftime('%d.%m.%Y, %H:%M Uhr'),
                                                          'header1': header1,
                                                          'header2': header2})
    response['Content-Type'] = 'image/svg+xml; charset=utf-8'
    response['Content-Disposition']  = 'attachment; filename=flyer-%s.svg'%v.datum.strftime('%Y%m')
    return response



