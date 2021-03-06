from django import template
from django.template.defaultfilters import stringfilter

import qrcode
import qrcode.image
import qrcode.image.svg
import xml.etree.ElementTree
from django.utils.safestring import mark_safe

from django.utils import timezone
from icalendar import Event

from textwrap import wrap

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

@register.filter('author_and_title')
def author_and_title(value, arg):
    """
    value = talk
    arg   = line length, font_size in px, linespacing in percents

    Formats the autor and title for a talk:
    if the title is longer than line length, the title will begin on the same line as the author name and be wrapped.
    in the other case, one line will be used for the author, the other for the title.
    """
    args = arg.split(',')
    line_length = int(args[0])
    font_size = float(args[1])
    linespacing = float(args[2])

    linespace = font_size * linespacing / 100

    if len(value.title) > line_length:
        wrapped = wrap('%s: %s'%(value.speaker, value.title), line_length)
        speaker_line = wrapped[0]
        # In case the wrapped version is longer than two lines, put the end of the title at the end of the second line.
        # It's then simpler to edit the SVG to get a pleasing document.
        title_line = ' '.join(wrapped[1:])
    else:
        speaker_line = value.speaker
        title_line = value.title
    return mark_safe('<tspan x="0" y="0">%s</tspan><tspan x="0" y="%f">%s</tspan>'%(speaker_line, linespace, title_line))

def format_event_date(value):
    """
    value = talk

    Formats the date range of an event
    """

    start_format = '%d.%m.%Y'
    end = ""
    if value.end:
        end = ' - %s'%value.end.strftime('%d.%m.%Y')
        # Now remove the redundant parts of the start date
        # Warning: UGLY
        if value.start.year == value.end.year:
            start_format = "%d.%m."
            if value.start.month == value.end.month:
                start_format = "%d."
                if value.start.day == value.end.day:
                    start_format = '%d.%m.%Y'
                    end = ""
    start = value.start.strftime(start_format)
    return '%s%s'%(start, end)

@register.filter('further_events')
def further_events(value, args):
    """
    value = talk
    arg   = line length, font_size in px, linespacing in percents

    Formats the further events
    """
    font_size = 15
    linespacing = 120
    result = []
    linespace =     font_size*linespacing/100
    for i, event in enumerate(value.event.all()[:2], 1):
        result.append("""<tspan x="0" y="%.1f">%s</tspan>"""%(linespace*i, format_event_date(event)))
        result.append("""<tspan x="140" y="%.1f">%s, %s</tspan>"""%(linespace*i, 
                                                                   event.title,
                                                                   event.location))
    return mark_safe("\n\t".join(result))
