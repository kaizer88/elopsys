# from django.utils.encoding import StrAndUnicode, force_unicode
from itertools import chain
from django.utils.safestring import mark_safe
from django.forms.widgets import CheckboxInput, CheckboxSelectMultiple
from django.utils.html import escape, conditional_escape

class CheckboxSelectMultipleWithMapButton(CheckboxSelectMultiple):

    def set_sda_mapping(self, sda_mapping):
        self.sda_mapping = sda_mapping

    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        output = [u'<ul>']
        # Normalize to strings
        str_values = set([force_unicode(v) for v in value])
        for i, (option_value, option_label) in enumerate(chain(self.choices, choices)):
            # If an ID attribute was given, add a numeric index as a suffix,
            # so that the checkboxes don't all have the same ID attribute.
            if has_id:
                final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
                label_for = u' for="%s"' % final_attrs['id']
            else:
                label_for = ''

            town_id = option_value
            if town_id in self.sda_mapping['town_maps'].keys() and self.sda_mapping['town_maps'][town_id] != '':
                rendered_map_button = """<button class='sda_map_button' onclick='return emerald.show_sda_map(event, "%s")'>map</button>""" % town_id
            else:
                rendered_map_button = """<button class='sda_map_button_disabled' onclick='return false'>map</button>"""

            cb = CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
            option_value = force_unicode(option_value)
            rendered_cb = cb.render(name, option_value)
            option_label = conditional_escape(force_unicode(option_label))

            output.append(u'<li><label%s>%s %s %s</label></li>' % (label_for, rendered_map_button, rendered_cb, option_label))
        output.append(u'</ul>')
        return mark_safe(u'\n'.join(output))

