from django import template
from django.template.defaultfilters import stringfilter

import qrcode
import qrcode.image
import qrcode.image.svg
import xml.etree.ElementTree
from django.utils.safestring import mark_safe

from django.utils import timezone
from icalendar import Event

register = template.Library()

class SvgGroup(qrcode.image.svg.SvgFragmentImage):
    """SVG image builder

    Creates a QR-code image as a SVG document fragment.
    Ignores the {box_size} parameter, making the QR-code boxes
    1mm square."""

    def __init__(self, border, width, box_size):
        super(SvgGroup, self).__init__(border, width, box_size)
        self.kind = "SVG"
        self._img = self._svg()

    def _svg(self, tag = "g"):
        return xml.etree.ElementTree.Element(tag)

    def _rect(self, row, col, tag="rect"):
        return xml.etree.ElementTree.Element(tag,
                          x="%d" % (self.border + col),
                          y="%d" % (self.border + row),
                          width="1", height="1")

    def _write(self, stream):
        xml.etree.ElementTree.ElementTree(self._img).write(stream, xml_declaration=False)

    def resize(self, size):
        """resize the code by applying a scale transform"""
        dimension = (2 * self.border + self.width)
        factor = size / dimension
        self._img.attrib['transform'] = 'scale(%f)' % factor

    def get_tree(self):
        return self._img

@register.filter(name='vevent')
def as_vevent(value):
    """Conver an event in to a vevent string"""
    event = Event()
    event.add('dtstamp', value.start)
    event.add('dtstart', value.start)
    event.add('duration', timezone.timedelta(hours=2, minutes=30))
    event.add('summary', value.title)
    event.add('description', value.presstext)
    
    return event.to_ical()

@register.filter(name='qrcode')
@stringfilter
def render_qrcode(value, arg='0,0'):
    """Converts a string in a SVG QRCode, the argument being the place for the code."""
    qr = qrcode.QRCode()
    qr.add_data(value)
    img = qr.make_image(image_factory=SvgGroup)
    img.resize(150)
    svg_tree = img.get_tree()
    
    return mark_safe(xml.etree.ElementTree.tostring(svg_tree))
