from django.shortcuts import render_to_response, get_object_or_404
from vortraegeapp.models import Vortrag
from textwrap import wrap

from django.template import Context, loader
from django.http import HttpResponse

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
    response = render_to_response('vortraege/pressetext.txt', {'vortrag': v,
                                                               'datum': v.datum.strftime('%A, %d. %B %Y')})
    response['Content-Type'] = 'text/plain; charset=utf-8'
    response['Content-Disposition']  = 'attachment; filename=pressetext-%s.txt'%v.datum.strftime('%Y%m')
    return response

def pdf_aushang(request, vortrag_id):
    v = get_object_or_404(Vortrag, pk=vortrag_id)

    t = loader.get_template('vortraege/aushang.svg')
    c = Context({'vortrag': v,
                 'datum': v.datum.strftime('%d.%m.%Y, %H:%M Uhr')})
    rendered =  t.render(c)

    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition']  = 'attachment; filename=aushang-%s.pdf'%v.datum.strftime('%Y%m')
    
    cairosvg.svg2pdf(bytestring=rendered.encode('utf-8'), write_to=response)

    return response
    
def svg_aushang(request, vortrag_id):
    v = get_object_or_404(Vortrag, pk=vortrag_id)

    t = loader.get_template('vortraege/aushang.svg')
    c = Context({'vortrag': v,
                 'datum': v.datum.strftime('%d.%m.%Y, %H:%M Uhr')})
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



