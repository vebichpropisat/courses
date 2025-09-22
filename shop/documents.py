from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl.registries import registry
from .models import Course
from django.utils.html import strip_tags

course_index = Index('courses')
course_index.settings(
    number_of_shards=1,
    number_of_replicas=0
)

@registry.register_document
class CourseDocument(Document):
    category = fields.ObjectField(properties={
        'title': fields.TextField(),
    })
    lecturer = fields.ObjectField(properties={
        'surname': fields.TextField(),
        'name': fields.TextField(),
    })
    description = fields.TextField()

    class Index:
        # Індекс
        name = 'courses'

    class Django:
        model = Course
        fields = [
            'title',
        ]

    def prepare_description(self, instance):
        return strip_tags(instance.description)