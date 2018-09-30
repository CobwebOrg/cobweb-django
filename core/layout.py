from typing import List, NamedTuple, Optional

from crispy_forms.layout import (
    BaseInput,
    Button,
    ButtonHolder,
    # Column,
    Div,
    Fieldset,
    HTML,
    Hidden,
    Layout,
    LayoutObject,
    MultiField,
    MultiWidgetField,
    Reset,
    Row,
    Submit,
    # TemplateNameMixin,
)
import crispy_forms.layout as crispy
from crispy_forms.bootstrap import (
    Accordion,
    AccordionGroup,
    Alert,
    AppendedText,
    Container,
    ContainerHolder,
    FieldWithButtons,
    FormActions,
    InlineCheckboxes,
    # InlineField,
    InlineRadios,
    PrependedAppendedText,
    PrependedText,
    StrictButton,
    Tab,
    TabHolder,
    UneditableField,
)
import crispy_forms.bootstrap as bootstrap


class Field(crispy.Field):
    def __init__(self, *args, show=True, edit=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.show = show
        self.edit = edit
        if not edit:
            self.attrs['disabled'] = True

    def render(self, form, form_style, context, template_pack='bootstrap4',
               extra_context=None, **kwargs):
        if not self.show:
            return ''
        else:
            return super().render(form, form_style, context, template_pack='bootstrap4',
                                  extra_context=None, **kwargs)


class InlineField(bootstrap.InlineField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'label' in kwargs:
            self.label = kwargs['label']


class FormSection(Div):
    def __init__(self, *args, **kwargs):
        try:
            kwargs['css_class'] += ' form-section'
        except KeyError:
            kwargs['css_class'] = 'form-section'
        super().__init__(*args, **kwargs)


def crawl_scope_fields(editable: bool=False) -> FormSection:
    return FormSection(
        Row(
            Column(Field('crawl_start_date', placeholder='YYYY-MM-DD',  edit=editable),
                   css_class='col-4'),
            Column(Field('crawl_end_date', placeholder='YYYY-MM-DD', edit=editable),
                   css_class='col-4'),
            Column(Field('crawl_frequency', edit=editable), css_class='col-4')
        ),
        Row(
            Column(
                Field('follow_links', edit=editable, css_class='mx-2 w-50',
                      template='field_inline.html'),
                css_class='col-6',
            ),
            Column(
                Field('page_scope', edit=editable, css_class='mx-2',
                      template='field_inline.html'),
                css_class='col-6',
            ),
            css_class='form-group form-inline',
        ),
        Field('ignore_robots_txt', edit=editable),
    )


title_plaintext_field = Layout(
    HTML("""
        {% load cobweb_look %}
        <h3 class="click_to_edit_field col-md-12 collapse show">
            {{object.title}}
            <a class="btn" data-toggle="collapse" href=".click_to_edit_field">
                {% icon 'edit' %}
            </a>
        </h3>
        """),
    Field('title', wrapper_class="col-md-12 click_to_edit_field collapse"),
)
title_form_field = Field('title', wrapper_class="col-md-12")


DEFAULT_TITLE = 'Save changes'
DEFAULT_TEXT = "Click the submit button to save changes, or click cancel to return to Cobweb without Saving."

def form_buttons(confirm_title=DEFAULT_TITLE, confirm_text=DEFAULT_TEXT) -> HTML:
    return HTML(f"""
        <div class="form-section form-button-row">
            <div class="row">
                <div class="col d-flex flex-row justify-content-end">
                    <button type="reset" class="btn btn-light btn-outline-dark mr-1">
                        Cancel
                    </button>
                    <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#exampleModal">
                        Submit
                    </button>
                </div>
            </div>
        </div>

        <!-- Modal for Confirmation Dialog -->
        <div class="modal fade" id="exampleModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLabel">{confirm_title}</h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    {confirm_text}
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-light btn-outline-dark mr-1" data-dismiss="modal">Cancel</button>
                    <input name="submit" value="Submit" class="btn btn-primary"
                           id="submit-id-submit" type="submit">
                </div>
                </div>
            </div>
        </div>
    """)


FORM_BUTTONS = form_buttons()


class Pane(Div):
    def __init__(self, *args, **kwargs):
        # try:
        #     kwargs['css_class'] += ' pane'
        # except KeyError:
        #     kwargs['css_class'] = 'pane'
        super().__init__(Div(*args, css_class='pane d-flex flex-column'), **kwargs)


class Column(Div):
    """
    Layout object. It wraps fields in a div whose default class is "col".

    For Cobweb, we override the default django_crispy_forms Column, which uses
    the bootstrap-incompatible class name "formColumn".

    Example::

        Column('form_field_1', 'form_field_2')
    """
    css_class = 'col'


class HField(Field):
    template = 'field_horizontal.html'


class InfoTab(NamedTuple):
    title: str
    content: LayoutObject


def tab_button(tab: InfoTab, tab_index: int) -> LayoutObject:
    return HTML(f"""
        <a class="nav-link{' active' if tab_index==0 else ''}"
           id="tab{tab_index}-tab" data-toggle="tab" href="#tab{tab_index}"
           role="tab" aria-controls="tab{tab_index}" aria-selected="true">
            {tab.title}
        </a>
    """)


def tab_panel(tab: InfoTab, tab_index: int) -> LayoutObject:
    return Layout(
        HTML(f"""<div class="tab-pane fade{' show active' if tab_index==0 else ''}"
                 id="tab{tab_index}" role="tabpanel" aria-labelledby="project-tab">"""),
        tab.content,
        HTML('</div>'),
    )


def info_tabs(*tabs: InfoTab) -> LayoutObject:
    return Layout(
        Div(
            *[tab_button(tab, i) for i, tab in enumerate(tabs)],
            css_class="nav nav-tabs nav-infotabs mb-4",
            css_id="myTab",
            role="tablist",
        ),
        Div(
            *[tab_panel(tab, i) for i, tab in enumerate(tabs)],
            css_class="tab-content", css_id="myTabContent",
        ),
    )


class BaseHeader(Layout):
    def __init__(self, *args, **kwargs):
        super().__init__(HTML(f'<h{self.n}>'), *
                         args, HTML(f'</h{self.n}>'), **kwargs)


class H1(BaseHeader):
    n = 1


class H2(BaseHeader):
    n = 2


class H3(BaseHeader):
    n = 3


class H4(BaseHeader):
    n = 4


class H5(BaseHeader):
    n = 5


class H6(BaseHeader):
    n = 6
