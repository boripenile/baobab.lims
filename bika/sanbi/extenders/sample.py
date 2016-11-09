from Products.Archetypes.references import HoldingReference
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from zope.component import adapts

from bika.lims.fields import *
from bika.lims.interfaces import ISample
from bika.lims.browser.widgets import ReferenceWidget as bika_ReferenceWidget

from bika.sanbi import bikaMessageFactory as _
from bika.sanbi.interfaces import IBioSpecimenStorage
import sys

from Products.Archetypes import atapi
from bika.lims.content.sample import Sample as BaseSample
from bika.lims.config import PROJECTNAME


class ExtFixedPointField(ExtensionField, FixedPointField):
    "Field extender"


class SampleSchemaExtender(object):
    adapts(ISample)
    implements(IOrderableSchemaExtender)

    fields = [
        ExtReferenceField(
            'Kit',
            vocabulary_display_path_bound=sys.maxint,
            allowed_types=('Kit',),
            relationship='SampleKit',
            referenceClass=HoldingReference,
            widget=bika_ReferenceWidget(
                label=_("Kit"),
                catalog_name='bika_catalog',
                visible={'view': 'invisible',
                         'edit': 'visible',
                         'header_table': 'visible',
                         'sample_registered': {'view': 'visible', 'edit': 'visible'},
                         'scheduled_sampling': {'view': 'visible', 'edit': 'visible'},
                         'sampled': {'view': 'visible', 'edit': 'visible'},
                         'sample_received': {'view': 'visible', 'edit': 'visible'},
                         'expired': {'view': 'visible', 'edit': 'visible'},
                         'disposed': {'view': 'visible', 'edit': 'visible'},
                         },
                render_own_label = True,
            )
        ),
        ExtReferenceField(
            'StorageLocation',
            allowed_types=('UnmanagedStorage', 'StoragePosition'),
            relationship='ItemStorageLocation',
            widget=bika_ReferenceWidget(
                label=_("Storage Location"),
                description=_("Location where item is kept"),
                size=40,
                visible={'edit': 'visible', 'view': 'visible'},
                catalog_name='bika_setup_catalog',
                showOn=True,
                render_own_label=True,
                base_query={'inactive_state': 'active',
                            'review_state': 'available',
                            'object_provides': IBioSpecimenStorage.__identifier__},
                colModel=[{'columnName': 'UID', 'hidden': True},
                          {'columnName': 'Title', 'width': '50', 'label': _('Title')},
                          {"columnName": "Hierarchy", "align": "left", "label": "Hierarchy", "width": "50"}
                          ],
            )
        ),
        ExtStringField(
            'SubjectID',
            searchable=True,
            widget=StringWidget(
                label=_("Subject ID"),
                description=_("Human-subject ID the specimen is taken from."),
                visible={'edit': 'visible',
                         'view': 'visible',
                         'header_table': 'visible',
                         'sample_registered': {'view': 'visible', 'edit': 'visible'},
                         'to_be_sampled': {'view': 'visible', 'edit': 'invisible'},
                         'scheduled_sampling': {'view': 'visible', 'edit': 'visible'},
                         'sampled': {'view': 'visible', 'edit': 'visible'},
                         'sample_received': {'view': 'visible', 'edit': 'visible'},
                         'expired': {'view': 'visible', 'edit': 'visible'},
                         'disposed': {'view': 'visible', 'edit': 'visible'},
                         },
                render_own_label=True,
            )
        ),
        ExtStringField(
            'Barcode',
            searchable=True,
            widget=StringWidget(
                label=_("Barcode"),
                description=_("Biospecimen barcode."),
                visible={'edit': 'visible',
                         'view': 'visible',
                         'header_table': 'visible',
                         'sample_registered': {'view': 'visible', 'edit': 'visible'},
                         'to_be_sampled': {'view': 'visible', 'edit': 'invisible'},
                         'scheduled_sampling': {'view': 'visible', 'edit': 'visible'},
                         'sampled': {'view': 'visible', 'edit': 'visible'},
                         'sample_received': {'view': 'visible', 'edit': 'visible'},
                         'expired': {'view': 'visible', 'edit': 'visible'},
                         'disposed': {'view': 'visible', 'edit': 'visible'},
                         },
                render_own_label=True,
            )
        ),
        ExtFixedPointField(
            'Volume',
            required=1,
            default="0.00",
            widget=DecimalWidget(
                label=_("Volume"),
                size=15,
                description=_("The The volume of the biospecimen taken from the subject."),
                visible={'edit': 'visible',
                         'view': 'visible',
                         'header_table': 'visible',
                         'sample_registered': {'view': 'visible', 'edit': 'visible'},
                         'to_be_sampled': {'view': 'visible', 'edit': 'invisible'},
                         'scheduled_sampling': {'view': 'visible', 'edit': 'visible'},
                         'sampled': {'view': 'visible', 'edit': 'visible'},
                         'sample_received': {'view': 'visible', 'edit': 'visible'},
                         'expired': {'view': 'visible', 'edit': 'visible'},
                         'disposed': {'view': 'visible', 'edit': 'visible'},
                         },
                render_own_label=True,
            )
        ),
        ExtStringField(
            'Unit',
            widget=StringWidget(
                label=_("Unit"),
                visible={'edit': 'visible',
                         'view': 'visible',
                         'header_table': 'visible',
                         'sample_registered': {'view': 'visible', 'edit': 'visible'},
                         'to_be_sampled': {'view': 'visible', 'edit': 'invisible'},
                         'scheduled_sampling': {'view': 'visible', 'edit': 'visible'},
                         'sampled': {'view': 'visible', 'edit': 'visible'},
                         'sample_received': {'view': 'visible', 'edit': 'visible'},
                         'expired': {'view': 'visible', 'edit': 'visible'},
                         'disposed': {'view': 'visible', 'edit': 'visible'},
                         },
                render_own_label=True,
            )
        ),
    ]

    def __init__(self, context):
        self.context = context

    def getOrder(self, schematas):
        return schematas

    def getFields(self):
        return self.fields

class SampleSchemaModifier(object):
    adapts(ISample)
    implements(ISchemaModifier)

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):
        return schema


class Sample(BaseSample):
    """ Inherits from bika.lims.content.sample
    """

# Overrides type bika.lims.content.sample
atapi.registerType(Sample, PROJECTNAME)
