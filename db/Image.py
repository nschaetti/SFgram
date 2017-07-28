
from mongoengine import *


# An image in the MongoDB database
class Image(Document):
    """
    A image in the MongoDB database.
    """

    # Indexes
    meta = {
        'indexes': [
            {
                'fields': ['#url']
            }]
    }

    # Fields
    image = FileField()
    url = StringField()
    extension = StringField()

    ###############################################
    # PUBLIC
    ###############################################

    # Does the image exists
    @staticmethod
    def exists(image_url):
        """
        Does country exists
        :param image_url:
        :return:
        """
        images = Image.objects(url=image_url)
        return images.count() > 0
    # end exists

    # Get image from url
    @staticmethod
    def get_by_url(image_url):
        """
        Get book from its title
        :param image_url:
        :return:
        """
        images = Image.objects(url=image_url)
        if images.count() > 0:
            return images[0]
        else:
            return None
        # end if
    # end get_by_url

# end Genre
