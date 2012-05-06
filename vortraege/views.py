from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from vortraege.models import Vortrag
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

    # The qrcode module tightly encapsulate its data,
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
    e.attrib['transform'] = 'translate(533.36055,279.81226)'

    t = loader.get_template('vortraege/aushang.svg')
    c = Context({'vortrag': v,
                 'datum': v.datum.strftime('%d.%m.%Y, %H:%M Uhr'),
                 'termin': mark_safe(xml.etree.ElementTree.tostring(e))})
    rendered =  t.render(c)

    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition']  = 'attachment; filename=aushang-%s.pdf'%v.datum.strftime('%Y%m')
    
    cairosvg.svg2pdf(bytestring=rendered.encode('utf-8'), write_to=response)

    return response
    
def svg_aushang(request, vortrag_id):
    v = get_object_or_404(Vortrag, pk=vortrag_id)

    #print request.build_absolute_uri(reverse('details', kwargs={'vortrag_id': vortrag_id}))

    # The qrcode module tightly encapsulate its data.
    temp_out = StringIO.StringIO()
    qr = qrcode.QRCode()
    qr.add_data('http://www.youtube.com/watch?v=Y1g2Cx03L2I')
    img = qr.make_image(image_factory=qrcode.image.svg.SvgFragmentImage)
    
    #img = qrcode.make('http://www.youtube.com/watch?v=Y1g2Cx03L2I')
    img.save(temp_out)
    #encoded = base64.b64encode(temp_out.getvalue())
    
    # Now change the XML so we can use it in the template
    e = xml.etree.ElementTree.fromstring(temp_out.getvalue())
    e.tag = '{http://www.w3.org/2000/svg}g'
    del e.attrib['version']
    e.attrib['transform'] = 'translate(533.36055,279.81226)'

    t = loader.get_template('vortraege/aushang.svg')
    c = Context({'vortrag': v,
                 'datum': v.datum.strftime('%d.%m.%Y, %H:%M Uhr'),
#                 'termin': mark_safe(temp_out.getvalue())})
                 'termin': mark_safe(xml.etree.ElementTree.tostring(e))})
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
                 'header2': header2})
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



