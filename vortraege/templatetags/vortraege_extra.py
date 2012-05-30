from django import template
from django.template.defaultfilters import stringfilter

import qrcode
import qrcode.image
import qrcode.image.svg
import StringIO
import xml.etree.ElementTree
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='qrcode')
@stringfilter
def render_qrcode(value, arg='0,0'):
    """Converts a string in a SVG QRCode, the argument being the place for the code."""
    # The qrcode module tightly encapsulate its data.
    # blocking changes to the generated svg,
    # which is why we go he StringIO way.
    temp_out = StringIO.StringIO()
    qr = qrcode.QRCode()
    qr.add_data(value)
    img = qr.make_image(image_factory=qrcode.image.svg.SvgFragmentImage)
    img.save(temp_out)
    
    # Now change the XML so we can use it in the template
    # ie: not a fragment.
    e = xml.etree.ElementTree.fromstring(temp_out.getvalue())
    e.tag = '{http://www.w3.org/2000/svg}g'
    del e.attrib['version']
    e.attrib['transform'] = 'translate(%s)'%arg
    return mark_safe(xml.etree.ElementTree.tostring(e))

@register.filter
def format_date(value, arg):
    """Format a date according to the template given as an argument"""
    return value.strftime(arg)
