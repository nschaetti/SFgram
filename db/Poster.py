
from mongoengine import *


# A movie poster in the MongoDB database
class Poster(Document):
    """
    A movie poster in the MongoDB database.
    """

    # Fields
    image = FileField()
    url = StringField()
    extension = StringField()

    ###############################################
    # PUBLIC
    ###############################################

    # Does a psoter exists
    @staticmethod
    def exists(image_url):
        """
        Does country exists
        :param image_url:
        :return:
        """
        images = Poster.objects(url=image_url)
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
        images = Poster.objects(url=image_url)
        if images.count() > 0:
            return images[0]
        else:
            return None
        # end if
    # end get_by_url

# end Genre
