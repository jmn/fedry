from rest_framework import serializers
from fd.models import FeedPost
from dj.settings.production import BLEACH_ALLOWED_TAGS, BLEACH_ALLOWED_ATTRIBUTES
import bleach

class PostSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()

    class Meta:
        model = FeedPost
        fields = ('id', 'feed', 'title', 'content', 'date_published')

    # http://www.django-rest-framework.org/api-guide/serializers/#dynamically-modifying-fields
    # DRF API "Subject to change" 
    def get_content(self, obj):
        return bleach.clean(obj.content,
                            tags=BLEACH_ALLOWED_TAGS,
                            attributes=BLEACH_ALLOWED_ATTRIBUTES,
                            strip=True)

