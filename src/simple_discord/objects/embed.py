import abc
import datetime
from typing import Optional, List, Dict

from .base_object import BaseDiscordObject
from . import enumerations


class Embed(BaseDiscordObject):

    title: Optional[str]
    type: Optional['enumerations.EMBED_TYPES']  # DEPRECATED
    description: Optional[str]                  # description of embed
    url: Optional[str]                          # url of embed
    timestamp: Optional['datetime.datetime']    # timestamp	timestamp of embed content
    color: Optional[int]                        # color code of the embed
    footer: Optional['EmbedFooter']             # footer information
    image: Optional['EmbedImage']               # image information
    thumbnail: Optional['EmbedThumbnail']       # thumbnail information
    video: Optional['EmbedVideo']               # video information
    provider: Optional['EmbedProvider']         # provider information
    author: Optional['EmbedAuthor']             # author information
    fields: Optional[List['EmbedField']]        # fields information

    def __str__(self):
        return 'Embed()'

    def to_dict(self) -> 'dict':  # noqa: C901
        new_dict: Dict[str, object] = dict()

        if hasattr(self, 'title'):
            new_dict['title'] = self.title
        if hasattr(self, 'type') and type(self.type) is enumerations.EMBED_TYPES:
            new_dict['type'] = self.type.name
        if hasattr(self, 'description'):
            new_dict['description'] = self.description
        if hasattr(self, 'url'):
            new_dict['url'] = self.url
        if hasattr(self, 'timestamp') and type(self.timestamp) is datetime.datetime:
            new_dict['timestamp'] = self.timestamp.isoformat()
        if hasattr(self, 'color'):
            new_dict['color'] = self.color
        if hasattr(self, 'footer') and type(self.footer) is EmbedFooter:
            new_dict['footer'] = self.footer.to_dict()
        if hasattr(self, 'image') and type(self.image) is EmbedImage:
            new_dict['image'] = self.image.to_dict()
        if hasattr(self, 'thumbnail') and type(self.thumbnail) is EmbedThumbnail:
            new_dict['thumbnail'] = self.thumbnail.to_dict()
        if hasattr(self, 'video') and type(self.video) is EmbedVideo:
            new_dict['video'] = self.video.to_dict()
        if hasattr(self, 'provider') and type(self.provider) is EmbedProvider:
            new_dict['provider'] = self.provider.to_dict()
        if hasattr(self, 'author') and type(self.author) is EmbedAuthor:
            new_dict['author'] = self.author.to_dict()
        if hasattr(self, 'fields') and type(self.fields) is list:
            new_dict['fields'] = list()
            assert type(new_dict['fields']) is list
            for field in self.fields:
                if type(field) is EmbedField:
                    new_dict['fields'].append(field.to_dict())

        return new_dict

    def generate(self,
                 title: Optional[str] = None,
                 type: Optional['enumerations.EMBED_TYPES'] = None,
                 description: Optional[str] = None,
                 url: Optional[str] = None,
                 timestamp: Optional['datetime.datetime'] = None,
                 color: Optional[int] = None,  # TODO: Support a rich color class here.
                 ):

        if title is not None:
            self.title = title

        if type is not None:
            self.type = type

        if description is not None:
            self.description = description

        if url is not None:
            self.url = url

        if timestamp is not None:
            self.timestamp = timestamp

        if color is not None:
            self.color = color

    def validate(self):

        total_length = 0

        if hasattr(self, 'title'):
            assert type(self.title) is str,\
                f'Got invalid type {type(self.title)} for title.'
            assert len(self.title) <= 256,\
                f'God invalid length of title, {len(self.title)} characters long. Max is 256.'
            total_length += len(self.title)

        if hasattr(self, 'type'):
            assert type(self.type) is enumerations.EMBED_TYPES,\
                f'Got invalid type {type(self.type)} for type.'

        if hasattr(self, 'description'):
            assert type(self.description) is str,\
                f'Got invalid type {type(self.description)} for description.'
            assert len(self.description) <= 4096,\
                f'Got invalid length of description, {len(self.description)} characters long. Max is 4096.'
            total_length += len(self.description)

        if hasattr(self, 'url'):
            assert type(self.url) is str,\
                f'Got invalid type {type(self.url)} for url.'

        if hasattr(self, 'timestamp'):
            assert type(self.timestamp) is datetime.datetime,\
                f'Got invalid type {type(self.timestamp)} for timestamp.'

        if hasattr(self, 'color'):
            assert type(self.color) is int,\
                f'Got invalid type {type(self.color)} for timestamp.'

        if hasattr(self, 'footer'):
            assert type(self.footer) is EmbedFooter,\
                f'Got invalid type {type(self.footer)} for footer. Must be EmbedFooter.'
            self.footer.validate()
            total_length += len(self.footer.text)

        if hasattr(self, 'fields'):
            assert type(self.fields) is list,\
                f'Got invalid type {type(self.fields)} for fields.'
            assert len(self.fields) <= 25,\
                f'Got invalid length of fields, {len(self.fields)} elements long. Max is 25.'
            for field in self.fields:
                field.validate()
                total_length += len(field.name)
                total_length += len(field.value)

        if hasattr(self, 'author'):
            assert type(self.author) is EmbedAuthor,\
                f'Got invalid type {type(self.author)} for author.'
            self.author.validate()

        assert total_length <= 6000,\
            f'Total characters in embed is {total_length}. Max API limit is 6000.'

    def add_footer(self,
                   text: str,
                   icon_url: str = None,
                   proxy_icon_url: str = None,
                   ) -> 'EmbedFooter':
        self.footer = EmbedFooter()
        self.footer.text = text
        if icon_url is not None:
            self.footer.icon_url = icon_url
        if proxy_icon_url is not None:
            self.footer.proxy_icon_url = proxy_icon_url
        return self.footer

    def add_image(self,
                  url: str,
                  proxy_url: str = None,
                  height: int = None,
                  width: int = None,
                  ) -> 'EmbedImage':
        self.image = EmbedImage()
        self.image.url = url
        if proxy_url is not None:
            self.image.proxy_url = proxy_url
        if height is not None:
            self.image.height = height
        if width is not None:
            self.image.width = width
        return self.image

    def add_thumbnail(self,
                      url: str,
                      proxy_url: str = None,
                      height: int = None,
                      width: int = None,
                      ) -> 'EmbedThumbnail':
        self.thumbnail = EmbedThumbnail()
        self.thumbnail.url = url
        if proxy_url is not None:
            self.thumbnail.proxy_url = proxy_url
        if height is not None:
            self.thumbnail.height = height
        if width is not None:
            self.thumbnail.width = width
        return self.thumbnail

    def add_video(self,
                  url: str,
                  proxy_url: str = None,
                  height: int = None,
                  width: int = None,
                  ) -> 'EmbedVideo':
        self.video = EmbedVideo()
        self.video.url = url
        if proxy_url is not None:
            self.video.proxy_url = proxy_url
        if height is not None:
            self.video.height = height
        if width is not None:
            self.video.width = width
        return self.video

    def add_provider(self,
                     name: Optional[str] = None,
                     url: Optional[str] = None,
                     ) -> 'EmbedProvider':
        self.provider = EmbedProvider()
        if name is not None:
            self.provider.name = name
        if url is not None:
            self.provider.url = url
        return self.provider

    def add_author(self,
                   name: str,
                   url: Optional[str] = None,
                   icon_url: Optional[str] = None,
                   proxy_icon_url: Optional[str] = None,
                   ) -> 'EmbedAuthor':
        self.author = EmbedAuthor()
        self.author.name = name
        if url is not None:
            self.author.url = url
        if icon_url is not None:
            self.author.icon_url = icon_url
        if proxy_icon_url is not None:
            self.author.proxy_icon_url = proxy_icon_url
        return self.author

    def add_field(self,
                  name: str,
                  value: str,
                  inline: bool = False,
                  ) -> 'EmbedField':
        if not hasattr(self, 'fields') or type(self.fields) is not list:
            self.fields = list()
        new_field = EmbedField()
        new_field.name = name
        new_field.value = value
        new_field.inline = inline
        self.fields.append(new_field)
        return new_field


class EmbedFooter(BaseDiscordObject):
    text: str  # footer text
    icon_url: Optional[str]  # url of footer icon (only supports http(s) and attachments)
    proxy_icon_url: Optional[str]  # a proxied url of footer icon

    def to_dict(self) -> 'dict':
        new_dict: Dict[str, object] = dict()
        if hasattr(self, 'text'):
            new_dict['text'] = self.text
        if hasattr(self, 'icon_url'):
            new_dict['icon_url'] = self.icon_url
        if hasattr(self, 'proxy_icon_url'):
            new_dict['proxy_icon_url'] = self.proxy_icon_url
        return new_dict

    def validate(self):

        assert len(self.text) <= 2048,\
            f'Got invalid length of text, {len(self.text)} elements long. Max is 2048.'

        if hasattr(self, 'icon_url'):
            assert type(self.icon_url) is str,\
                f'Got invalid type {type(self.icon_url)} for icon_url. Must be str.'
            assert self.icon_url.startswith(('http://', 'https://')),\
                f'Got invalid icon_url {self.icon_url}, must start with http:// or https://.'

        if hasattr(self, 'proxy_icon_url'):
            assert type(self.proxy_icon_url) is str,\
                f'Got invalid type {type(self.proxy_icon_url)} for proxy_icon_url. Must be str.'
            assert self.proxy_icon_url.startswith(('http://', 'https://')),\
                f'Got invalid proxy_icon_url {self.proxy_icon_url}, must start with http:// or https://.'


class EmbedImage(BaseDiscordObject):

    url: str  # source url of thumbnail (only supports http(s) and attachments)
    proxy_url: Optional[str]  # a proxied url of the thumbnail
    height: Optional[int]  # height of thumbnail
    width: Optional[int]  # width of thumbnail

    def to_dict(self) -> 'dict':

        new_dict: Dict[str, object] = dict()
        new_dict['url'] = self.url

        if hasattr(self, 'proxy_url'):
            new_dict['proxy_url'] = self.proxy_url

        if hasattr(self, 'height'):
            new_dict['height'] = self.height

        if hasattr(self, 'width'):
            new_dict['width'] = self.width

        return new_dict

    def validate(self):

        assert type(self.url) is str,\
            f'Got invalid type {type(self.url)} for url. Must be str.'
        assert self.url.startswith(('http://', 'https://')),\
            f'Got invalid url {self.url}, must start with http:// or https://.'

        if hasattr(self, 'proxy_url'):
            assert type(self.proxy_url) is str,\
                f'Got invalid type {type(self.proxy_url)} for proxy_url. Must be str.'
            assert self.proxy.startswith(('http://', 'https://')),\
                f'Got invalid proxy {self.proxy}, must start with http:// or https://.'

        if hasattr(self, 'height'):
            assert type(self.height) is int,\
                f'Got invalid type {type(self.height)} for height. Must be int.'

        if hasattr(self, 'width'):
            assert type(self.width) is int,\
                f'Got invalid type {type(self.width)} for url. Must be int.'


class EmbedThumbnail(BaseDiscordObject):

    url: str  # source url of thumbnail (only supports http(s) and attachments)
    proxy_url: Optional[str]  # a proxied url of the thumbnail
    height: Optional[int]  # height of thumbnail
    width: Optional[int]  # width of thumbnail

    def to_dict(self) -> 'dict':

        new_dict: Dict[str, object] = dict()
        new_dict['url'] = self.url

        if hasattr(self, 'proxy_url'):
            new_dict['proxy_url'] = self.proxy_url

        if hasattr(self, 'height'):
            new_dict['height'] = self.height

        if hasattr(self, 'width'):
            new_dict['width'] = self.width

        return new_dict

    def validate(self):

        assert type(self.url) is str,\
            f'Got invalid type {type(self.url)} for url. Must be str.'
        assert self.url.startswith(('http://', 'https://')),\
            f'Got invalid url {self.url}, must start with http:// or https://.'

        if hasattr(self, 'proxy_url'):
            assert type(self.proxy_url) is str,\
                f'Got invalid type {type(self.proxy_url)} for proxy_url. Must be str.'
            assert self.proxy_url.startswith(('http://', 'https://')),\
                f'Got invalid proxy_url {self.proxy_url}, must start with http:// or https://.'

        if hasattr(self, 'height'):
            assert type(self.height) is int,\
                f'Got invalid type {type(self.height)} for height. Must be int.'

        if hasattr(self, 'width'):
            assert type(self.width) is int,\
                f'Got invalid type {type(self.width)} for url. Must be int.'


class EmbedVideo(BaseDiscordObject):

    url: Optional[str]  # source url of thumbnail (only supports http(s) and attachments)
    proxy_url: Optional[str]  # a proxied url of the thumbnail
    height: Optional[int]  # height of thumbnail
    width: Optional[int]  # width of thumbnail

    def to_dict(self) -> 'dict':

        new_dict: Dict[str, object] = dict()
        if hasattr(self, 'url'):
            new_dict['url'] = self.url

        if hasattr(self, 'proxy_url'):
            new_dict['proxy_url'] = self.proxy_url

        if hasattr(self, 'height'):
            new_dict['height'] = self.height

        if hasattr(self, 'width'):
            new_dict['width'] = self.width

        return new_dict

    def validate(self):

        if hasattr(self, 'url'):
            assert type(self.url) is str,\
                f'Got invalid type {type(self.url)} for url. Must be str.'
            assert self.url.startswith(('http://', 'https://')),\
                f'Got invalid url {self.url}, must start with http:// or https://.'

        if hasattr(self, 'proxy_url'):
            assert type(self.proxy_url) is str,\
                f'Got invalid type {type(self.proxy_url)} for proxy_url. Must be str.'
            assert self.proxy_url.startswith(('http://', 'https://')),\
                f'Got invalid proxy_url {self.proxy_url}, must start with http:// or https://.'

        if hasattr(self, 'height'):
            assert type(self.height) is int,\
                f'Got invalid type {type(self.height)} for height. Must be int.'

        if hasattr(self, 'width'):
            assert type(self.width) is int,\
                f'Got invalid type {type(self.width)} for url. Must be int.'


class EmbedProvider(BaseDiscordObject):
    name: str  # name of author
    url: str  # url of author

    def to_dict(self) -> 'dict':
        new_dict: Dict[str, object] = dict()

        if hasattr(self, 'name'):
            new_dict['name'] = self.name

        if hasattr(self, 'url'):
            new_dict['url'] = self.url
        return new_dict

    def validate(self):
        if hasattr(self, 'name'):
            assert type(self.name) is str,\
                f'Got invalid type {type(self.name)} for name. Must be str.'
            assert len(self.name) <= 256,\
                f'Got invalid length of name, {len(self.name)} characters long. Max is 256.'

        if hasattr(self, 'url'):
            assert type(self.url) is str,\
                f'Got invalid type {type(self.url)} for url. Must be str.'
            assert self.url.startswith(('http://', 'https://')),\
                f'Got invalid url {self.url}, must start with http:// or https://.'


class EmbedAuthor(BaseDiscordObject):
    name: str  # name of author
    url: str  # url of author
    icon_url: str  # url of author icon (only supports http(s) and attachments)
    proxy_icon_url: str  # a proxied url of author icon

    def to_dict(self) -> 'dict':
        new_dict: Dict[str, object] = dict()

        if hasattr(self, 'name'):
            new_dict['name'] = self.name

        if hasattr(self, 'url'):
            new_dict['url'] = self.url

        if hasattr(self, 'icon_url'):
            new_dict['icon_url'] = self.icon_url

        if hasattr(self, 'proxy_icon_url'):
            new_dict['proxy_icon_url'] = self.proxy_icon_url

        return new_dict

    def validate(self):
        if hasattr(self, 'name'):
            assert type(self.name) is str,\
                f'Got invalid type {type(self.name)} for name. Must be str.'
            assert len(self.name) <= 256,\
                f'Got invalid length of name, {len(self.name)} characters long. Max is 256.'

        if hasattr(self, 'url'):
            assert type(self.url) is str,\
                f'Got invalid type {type(self.url)} for url. Must be str.'
            assert self.url.startswith(('http://', 'https://')),\
                f'Got invalid url {self.url}, must start with http:// or https://.'

        if hasattr(self, 'icon_url'):
            assert type(self.icon_url) is str,\
                f'Got invalid type {type(self.icon_url)} for icon_url. Must be str.'
            assert self.icon_url.startswith(('http://', 'https://')),\
                f'Got invalid icon_url {self.icon_url}, must start with http:// or https://.'

        if hasattr(self, 'proxy_icon_url'):
            assert type(self.proxy_icon_url) is str,\
                f'Got invalid type {type(self.proxy_icon_url)} for proxy_icon_url. Must be str.'
            assert self.proxy_icon_url.startswith(('http://', 'https://')),\
                f'Got invalid proxy_icon_url {self.proxy_icon_url}, must start with http:// or https://.'


class EmbedField(BaseDiscordObject):
    name: str               # name of the field
    value: str              # value of the field
    inline: bool            # whether or not this field should display inline

    def to_dict(self) -> 'dict':
        new_dict: Dict[str, object] = dict()

        if hasattr(self, 'name'):
            new_dict['name'] = self.name

        if hasattr(self, 'value'):
            new_dict['value'] = self.value

        if hasattr(self, 'inline'):
            new_dict['inline'] = self.inline

        return new_dict

    def validate(self):
        if hasattr(self, 'name'):
            assert type(self.name) is str,\
                f'Got invalid type {type(self.name)} for name. Must be str.'
            assert len(self.name) <= 256,\
                f'Got invalid length of name, {len(self.name)} characters long. Max is 256.'

        if hasattr(self, 'value'):
            assert type(self.value) is str,\
                f'Got invalid type {type(self.value)} for value. Must be str.'
            assert len(self.value) <= 1024,\
                f'Got invalid length of value, {len(self.value)} characters long. Max is 1024.'

        if hasattr(self, 'inline'):
            assert type(self.inline) is bool,\
                f'Got invalid type {type(self.inline)} for inline. Must be bool.'


class EmbedAdder(abc.ABC):

    '''Allow other objects to start adding components to themselves with a common set of helper functions.

    Caution: This is an abstract class, and is not intended for direct instantiation.
    '''

    def add_embeds(self) -> 'Embed':
        '''
        Start adding components by starting an ACTION_ROW.
        '''
        if not hasattr(self, 'embeds'):
            self.embeds: Optional[List['Embed']] = list()
        assert type(self.embeds) is list
        new_embed = Embed()
        self.embeds.append(new_embed)

        return new_embed
