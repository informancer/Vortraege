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
def render_qrcode(value):
    """Converts a string in a SVG QRCode"""
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
    # That should be inside the template.
    e.attrib['transform'] = 'translate(533.36055,279.81226)'
    return mark_safe(xml.etree.ElementTree.tostring(e))
