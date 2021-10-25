import abc
import datetime
from typing import Optional, List, Dict

import validators  # type: ignore

from .base_object import BaseDiscordObject
from . import enumerations


class Embed(BaseDiscordObject):
    '''Rich context holder for a message.'''

    EMBED_TYPES = enumerations.EMBED_TYPES

    title: Optional[str] = None
    type: Optional['enumerations.EMBED_TYPES'] = None  # type: ignore # DEPRECATED
    description: Optional[str] = None  # type: ignore # description of embed
    url: Optional[str] = None  # type: ignore # url of embed
    timestamp: Optional['datetime.datetime'] = None  # type: ignore # timestamp	timestamp of embed content
    color: Optional[int] = None  # type: ignore # color code of the embed
    footer: Optional['EmbedFooter'] = None  # type: ignore # footer information
    image: Optional['EmbedImage'] = None  # type: ignore # image information
    thumbnail: Optional['EmbedThumbnail'] = None  # type: ignore # thumbnail information
    video: Optional['EmbedVideo'] = None  # type: ignore # video information
    provider: Optional['EmbedProvider'] = None  # type: ignore # provider information
    author: Optional['EmbedAuthor'] = None  # type: ignore # author information
    fields: Optional[List['EmbedField']] = None  # type: ignore # fields information

    def __str__(self):
        '''Return string representation.'''
        return 'Embed()'

    def to_dict(self) -> 'dict':  # noqa: C901
        '''Convert object to dictionary suitable for API or other generic useage.'''
        new_dict: Dict[str, object] = dict()

        if (self.title is not None):
            new_dict['title'] = self.title
        if (self.type is not None) and (type(self.type) is enumerations.EMBED_TYPES):
            new_dict['type'] = self.type.name
        if (self.description is not None):
            new_dict['description'] = self.description
        if (self.url is not None):
            new_dict['url'] = self.url
        if (self.timestamp is not None) and (type(self.timestamp) is datetime.datetime):
            new_dict['timestamp'] = self.timestamp.isoformat()
        if (self.color is not None):
            new_dict['color'] = self.color
        if (self.footer is not None) and (type(self.footer) is EmbedFooter):
            new_dict['footer'] = self.footer.to_dict()
        if (self.image is not None) and (type(self.image) is EmbedImage):
            new_dict['image'] = self.image.to_dict()
        if (self.thumbnail is not None) and (type(self.thumbnail) is EmbedThumbnail):
            new_dict['thumbnail'] = self.thumbnail.to_dict()
        if (self.video is not None) and (type(self.video) is EmbedVideo):
            new_dict['video'] = self.video.to_dict()
        if (self.provider is not None) and (type(self.provider) is EmbedProvider):
            new_dict['provider'] = self.provider.to_dict()
        if (self.author is not None) and (type(self.author) is EmbedAuthor):
            new_dict['author'] = self.author.to_dict()
        if (self.fields is not None) and (type(self.fields) is list):
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
        '''Generate various elements of an Embed.'''
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

    def validate(self):  # noqa: C901
        '''Validate object is prepared for dispatch to discord.'''
        total_length = 0

        if self.title is not None:
            assert type(self.title) is str,\
                f'Got invalid type {type(self.title)} for title.'
            assert len(self.title) <= 256,\
                f'God invalid length of title, {len(self.title)} characters long. Max is 256.'
            total_length += len(self.title)

        if self.type is not None:
            assert type(self.type) is enumerations.EMBED_TYPES,\
                f'Got invalid type {type(self.type)} for type.'

        if self.description is not None:
            assert type(self.description) is str,\
                f'Got invalid type {type(self.description)} for description.'
            assert len(self.description) <= 4096,\
                f'Got invalid length of description, {len(self.description)} characters long. Max is 4096.'
            total_length += len(self.description)

        if self.url is not None:
            assert type(self.url) is str,\
                f'Got invalid type {type(self.url)} for url.'
            if not validators.url(self.url, public=False):
                raise AssertionError(f'URL fails validation: [{self.url}].')

        if self.timestamp is not None:
            assert type(self.timestamp) is datetime.datetime,\
                f'Got invalid type {type(self.timestamp)} for timestamp.'

        if self.color is not None:
            assert type(self.color) is int,\
                f'Got invalid type {type(self.color)} for timestamp.'

        if self.footer is not None:
            assert type(self.footer) is EmbedFooter,\
                f'Got invalid type {type(self.footer)} for footer. Must be EmbedFooter.'
            self.footer.validate()
            total_length += len(self.footer.text)

        if self.fields is not None:
            assert type(self.fields) is list,\
                f'Got invalid type {type(self.fields)} for fields.'
            assert len(self.fields) <= 25,\
                f'Got invalid length of fields, {len(self.fields)} elements long. Max is 25.'
            for field in self.fields:
                field.validate()
                total_length += len(field.name)
                total_length += len(field.value)

        if self.author is not None:
            assert type(self.author) is EmbedAuthor,\
                f'Got invalid type {type(self.author)} for author.'
            self.author.validate()

        if self.image is not None:
            assert type(self.image) is EmbedImage,\
                f'Got invalid type {type(self.image)} for image.'
            self.image.validate()

        if self.thumbnail is not None:
            assert type(self.thumbnail) is EmbedThumbnail,\
                f'Got invalid type {type(self.thumbnail)} for thumbnail.'
            self.thumbnail.validate()

        if self.video is not None:
            assert type(self.video) is EmbedVideo,\
                f'Got invalid type {type(self.video)} for video.'
            self.video.validate()

        if self.provider is not None:
            assert type(self.provider) is EmbedProvider,\
                f'Got invalid type {type(self.provider)} for provider.'
            self.provider.validate()

        assert total_length <= 6000,\
            f'Total characters in embed is {total_length}. Max API limit is 6000.'

    def add_footer(self,
                   text: str,
                   icon_url: str = None,
                   proxy_icon_url: str = None,
                   ) -> 'EmbedFooter':
        '''Add footer to the Embed.'''
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
        '''Add image to the Embed.'''
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
        '''Add thumbnail to the Embed.'''
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
        '''Add video to the Embed.'''
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
        '''Add provider to the Embed.'''
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
        '''Add author to the Embed.'''
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
        '''Add a generic field to the Embed.'''
        if not isinstance(self.fields, list):
            self.fields = list()
        new_field = EmbedField()
        new_field.name = name
        new_field.value = value
        new_field.inline = inline
        self.fields.append(new_field)
        return new_field


class EmbedFooter(BaseDiscordObject):
    '''Footer details for the Embed.'''

    text: str = None  # type: ignore  # footer text
    icon_url: Optional[str] = None  # url of footer icon (only supports http(s) and attachments)
    proxy_icon_url: Optional[str] = None  # a proxied url of footer icon

    def to_dict(self) -> 'dict':
        '''Convert object to dictionary suitable for API or other generic useage.'''
        new_dict: Dict[str, object] = dict()
        if self.text is not None:
            new_dict['text'] = self.text
        if self.icon_url is not None:
            new_dict['icon_url'] = self.icon_url
        if self.proxy_icon_url is not None:
            new_dict['proxy_icon_url'] = self.proxy_icon_url
        return new_dict

    def validate(self):
        '''Validate object is prepared for dispatch to discord.'''
        assert len(self.text) <= 2048,\
            f'Got invalid length of text, {len(self.text)} elements long. Max is 2048.'

        if self.icon_url is not None:
            assert type(self.icon_url) is str,\
                f'Got invalid type {type(self.icon_url)} for icon_url. Must be str.'
            assert self.icon_url.startswith(('http://', 'https://')),\
                f'Got invalid icon_url {self.icon_url}, must start with http:// or https://.'

        if self.proxy_icon_url is not None:
            assert type(self.proxy_icon_url) is str,\
                f'Got invalid type {type(self.proxy_icon_url)} for proxy_icon_url. Must be str.'
            assert self.proxy_icon_url.startswith(('http://', 'https://')),\
                f'Got invalid proxy_icon_url {self.proxy_icon_url}, must start with http:// or https://.'


class EmbedImage(BaseDiscordObject):
    '''Image to embed.'''

    url: str = None  # type: ignore  # source url of thumbnail (only supports http(s) and attachments)
    proxy_url: Optional[str] = None  # a proxied url of the thumbnail
    height: Optional[int] = None  # height of thumbnail
    width: Optional[int] = None  # width of thumbnail

    def to_dict(self) -> 'dict':
        '''Convert object to dictionary suitable for API or other generic useage.'''
        new_dict: Dict[str, object] = dict()
        new_dict['url'] = self.url

        if self.proxy_url is not None:
            new_dict['proxy_url'] = self.proxy_url

        if self.height is not None:
            new_dict['height'] = self.height

        if self.width is not None:
            new_dict['width'] = self.width

        return new_dict

    def validate(self):
        '''Validate object is prepared for dispatch to discord.'''
        assert type(self.url) is str,\
            f'Got invalid type {type(self.url)} for url. Must be str.'
        assert self.url.startswith(('http://', 'https://')),\
            f'Got invalid url {self.url}, must start with http:// or https://.'

        if self.proxy_url is not None:
            assert type(self.proxy_url) is str,\
                f'Got invalid type {type(self.proxy_url)} for proxy_url. Must be str.'
            assert self.proxy_url.startswith(('http://', 'https://')),\
                f'Got invalid proxy {self.proxy_url}, must start with http:// or https://.'

        if self.height is not None:
            assert type(self.height) is int,\
                f'Got invalid type {type(self.height)} for height. Must be int.'

        if self.width is not None:
            assert type(self.width) is int,\
                f'Got invalid type {type(self.width)} for url. Must be int.'


class EmbedThumbnail(BaseDiscordObject):
    '''Thumbnail to embed.'''

    url: str = None  # type: ignore  # source url of thumbnail (only supports http(s) and attachments)
    proxy_url: Optional[str] = None  # a proxied url of the thumbnail
    height: Optional[int] = None  # height of thumbnail
    width: Optional[int] = None  # width of thumbnail

    def to_dict(self) -> 'dict':
        '''Convert object to dictionary suitable for API or other generic useage.'''
        new_dict: Dict[str, object] = dict()
        new_dict['url'] = self.url

        if self.proxy_url is not None:
            new_dict['proxy_url'] = self.proxy_url

        if self.height is not None:
            new_dict['height'] = self.height

        if self.width is not None:
            new_dict['width'] = self.width

        return new_dict

    def validate(self):
        '''Validate object is prepared for dispatch to discord.'''
        assert type(self.url) is str,\
            f'Got invalid type {type(self.url)} for url. Must be str.'
        assert self.url.startswith(('http://', 'https://')),\
            f'Got invalid url {self.url}, must start with http:// or https://.'

        if self.proxy_url is not None:
            assert type(self.proxy_url) is str,\
                f'Got invalid type {type(self.proxy_url)} for proxy_url. Must be str.'
            assert self.proxy_url.startswith(('http://', 'https://')),\
                f'Got invalid proxy_url {self.proxy_url}, must start with http:// or https://.'

        if self.height is not None:
            assert type(self.height) is int,\
                f'Got invalid type {type(self.height)} for height. Must be int.'

        if self.width is not None:
            assert type(self.width) is int,\
                f'Got invalid type {type(self.width)} for url. Must be int.'


class EmbedVideo(BaseDiscordObject):
    '''Video to embed.'''

    url: Optional[str] = None  # source url of thumbnail (only supports http(s) and attachments)
    proxy_url: Optional[str] = None  # a proxied url of the thumbnail
    height: Optional[int] = None  # height of thumbnail
    width: Optional[int] = None  # width of thumbnail

    def to_dict(self) -> 'dict':
        '''Convert object to dictionary suitable for API or other generic useage.'''
        new_dict: Dict[str, object] = dict()
        if self.url is not None:
            new_dict['url'] = self.url

        if self.proxy_url is not None:
            new_dict['proxy_url'] = self.proxy_url

        if self.height is not None:
            new_dict['height'] = self.height

        if self.width is not None:
            new_dict['width'] = self.width

        return new_dict

    def validate(self):
        '''Validate object is prepared for dispatch to discord.'''
        if self.url is not None:
            assert type(self.url) is str,\
                f'Got invalid type {type(self.url)} for url. Must be str.'
            assert self.url.startswith(('http://', 'https://')),\
                f'Got invalid url {self.url}, must start with http:// or https://.'

        if self.proxy_url is not None:
            assert type(self.proxy_url) is str,\
                f'Got invalid type {type(self.proxy_url)} for proxy_url. Must be str.'
            assert self.proxy_url.startswith(('http://', 'https://')),\
                f'Got invalid proxy_url {self.proxy_url}, must start with http:// or https://.'

        if self.height is not None:
            assert type(self.height) is int,\
                f'Got invalid type {type(self.height)} for height. Must be int.'

        if self.width is not None:
            assert type(self.width) is int,\
                f'Got invalid type {type(self.width)} for url. Must be int.'


class EmbedProvider(BaseDiscordObject):
    '''Provider of the content from the Embed.'''

    name: str = None  # type: ignore  # name of author
    url: str = None  # type: ignore  # url of author

    def to_dict(self) -> 'dict':
        '''Convert object to dictionary suitable for API or other generic useage.'''
        new_dict: Dict[str, object] = dict()

        if self.name is not None:
            new_dict['name'] = self.name

        if self.url is not None:
            new_dict['url'] = self.url
        return new_dict

    def validate(self):
        '''Validate object is prepared for dispatch to discord.'''
        if self.name is not None:
            assert type(self.name) is str,\
                f'Got invalid type {type(self.name)} for name. Must be str.'
            assert len(self.name) <= 256,\
                f'Got invalid length of name, {len(self.name)} characters long. Max is 256.'

        if self.url is not None:
            assert type(self.url) is str,\
                f'Got invalid type {type(self.url)} for url. Must be str.'
            assert self.url.startswith(('http://', 'https://')),\
                f'Got invalid url {self.url}, must start with http:// or https://.'


class EmbedAuthor(BaseDiscordObject):
    '''Author of the content from the Embed.'''

    name: str = None  # type: ignore  # name of author
    url: str = None  # type: ignore  # url of author
    icon_url: str = None  # type: ignore  # url of author icon (only supports http(s) and attachments)
    proxy_icon_url: str = None  # type: ignore  # a proxied url of author icon

    def to_dict(self) -> 'dict':
        '''Convert object to dictionary suitable for API or other generic useage.'''
        new_dict: Dict[str, object] = dict()

        if self.name is not None:
            new_dict['name'] = self.name

        if self.url is not None:
            new_dict['url'] = self.url

        if self.icon_url is not None:
            new_dict['icon_url'] = self.icon_url

        if self.proxy_icon_url is not None:
            new_dict['proxy_icon_url'] = self.proxy_icon_url

        return new_dict

    def validate(self):
        '''Validate object is prepared for dispatch to discord.'''
        if self.name is not None:
            assert type(self.name) is str,\
                f'Got invalid type {type(self.name)} for name. Must be str.'
            assert len(self.name) <= 256,\
                f'Got invalid length of name, {len(self.name)} characters long. Max is 256.'

        if self.url is not None:
            assert type(self.url) is str,\
                f'Got invalid type {type(self.url)} for url. Must be str.'
            assert self.url.startswith(('http://', 'https://')),\
                f'Got invalid url {self.url}, must start with http:// or https://.'

        if self.icon_url is not None:
            assert type(self.icon_url) is str,\
                f'Got invalid type {type(self.icon_url)} for icon_url. Must be str.'
            assert self.icon_url.startswith(('http://', 'https://')),\
                f'Got invalid icon_url {self.icon_url}, must start with http:// or https://.'

        if self.proxy_icon_url is not None:
            assert type(self.proxy_icon_url) is str,\
                f'Got invalid type {type(self.proxy_icon_url)} for proxy_icon_url. Must be str.'
            assert self.proxy_icon_url.startswith(('http://', 'https://')),\
                f'Got invalid proxy_icon_url {self.proxy_icon_url}, must start with http:// or https://.'


class EmbedField(BaseDiscordObject):
    '''Single field of an Embed.'''

    name: str = None  # type: ignore # name of the field
    value: str = None  # type: ignore # value of the field
    inline: bool = None  # type: ignore # whether or not this field should display inline

    def to_dict(self) -> 'dict':
        '''Convert object to dictionary suitable for API or other generic useage.'''
        new_dict: Dict[str, object] = dict()

        if self.name is not None:
            new_dict['name'] = self.name

        if self.value is not None:
            new_dict['value'] = self.value

        if self.inline is not None:
            new_dict['inline'] = self.inline

        return new_dict

    def validate(self):
        '''Validate object is prepared for dispatch to discord.'''
        if self.name is not None:
            assert type(self.name) is str,\
                f'Got invalid type {type(self.name)} for name. Must be str.'
            assert len(self.name) <= 256,\
                f'Got invalid length of name, {len(self.name)} characters long. Max is 256.'

        if self.value is not None:
            assert type(self.value) is str,\
                f'Got invalid type {type(self.value)} for value. Must be str.'
            assert len(self.value) <= 1024,\
                f'Got invalid length of value, {len(self.value)} characters long. Max is 1024.'

        if self.inline is not None:
            assert type(self.inline) is bool,\
                f'Got invalid type {type(self.inline)} for inline. Must be bool.'


class EmbedAdder(abc.ABC):
    '''Allow other objects to start adding components to themselves with a common set of helper functions.

    Caution: This is an abstract class, and is not intended for direct instantiation.
    '''

    embeds: Optional[List['Embed']] = None

    def add_embeds(self) -> 'Embed':
        '''Add embeds to the object.'''
        if not isinstance(self.embeds, list):
            self.embeds: Optional[List['Embed']] = list()
        assert type(self.embeds) is list
        new_embed = Embed()
        self.embeds.append(new_embed)

        return new_embed
