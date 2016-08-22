# -*- coding: utf-8 -*-

from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from ..abstract_models import FedoraDated
from ..fedora.modelmixins import FedoraMixin

from .core import Author
from .core import Collection
from .core import EruditDocument


class SearchUnit(FedoraMixin, FedoraDated):
    """ A simple search unit. """

    collection = models.ForeignKey(
        Collection, related_name='search_units', verbose_name=_('Collection'))
    """ The collection associated with the search unit. """

    code = models.SlugField(
        max_length=255, unique=True, db_index=True, verbose_name=_('Code'), help_text=_('Code'))
    """ The shortname of the search unit. """

    localidentifier = models.CharField(
        max_length=100, unique=True, db_index=True, verbose_name=_('Identifiant unique'))
    """ The unique identifier of the search unit (it can be a Fedora identifier). """

    name = models.CharField(max_length=255, verbose_name=_('Nom'))
    """ The name of the search unit. """

    subname = models.CharField(max_length=400, verbose_name=_('Nom complet'), blank=True, null=True)
    """ The subname of the search unit (optional). """

    description = models.TextField(verbose_name=_('Description'), blank=True, null=True)
    """ The description of the search unit (optional). """

    first_publication_year = models.PositiveIntegerField(
        verbose_name=_('Première année de publication'), blank=True, null=True)
    """ The first year when a document of this search unit has been published. """

    last_publication_year = models.PositiveIntegerField(
        verbose_name=_('Dernière année de publication'), blank=True, null=True)
    """ The last year when a document of this search unit has been published. """

    class Meta:
        ordering = ('name', )
        verbose_name = _('Unité de recherche')
        verbose_name_plural = _('Unités de recherche')

    def __str__(self):
        return '{:s} [{:s}]'.format(self.name, self.code)

    @cached_property
    def documents_count(self):
        return SearchUnitDocument.objects.filter(collection__search_unit_id=self.id).count()


class SearchUnitCollection(FedoraMixin, FedoraDated):
    """ A simple search unit collection. """

    search_unit = models.ForeignKey(
        SearchUnit, related_name='collections', verbose_name=_('Unité de recherche'))
    """ The search unit associated with this collection. """

    localidentifier = models.CharField(
        max_length=100, unique=True, db_index=True, verbose_name=_('Identifiant unique'))
    """ The unique identifier of the collection (it can be a Fedora identifier). """

    title = models.CharField(max_length=400, verbose_name=_('Titre'))
    """ The title of this collection. """

    description = models.TextField(verbose_name=_('Description'), blank=True, null=True)
    """ The description of this collection. """

    class Meta:
        ordering = ('title', )
        verbose_name = _("Collection d'unité de recherche")
        verbose_name_plural = _("Collections d'unités de recherche")

    def __str__(self):
        return self.title


class SearchUnitDocument(EruditDocument, FedoraMixin, FedoraDated):
    """ A simple search unit document. """

    collection = models.ForeignKey(
        SearchUnitCollection, related_name='documents', verbose_name=_('Collection'))
    """ The collection associated with this document. """

    title = models.CharField(max_length=400, verbose_name=_('Titre'))
    """ The title of the document. """

    abstract = models.TextField(verbose_name=_('Résumé'))
    """ The abstract of the document. """

    publication_year = models.PositiveIntegerField(verbose_name=_('Année de publication'))
    """ The publication year of the document. """

    authors = models.ManyToManyField(Author, verbose_name=_('Auteurs'))
    """ A document can have many authors. """

    description_url = models.URLField(
        verbose_name=_('URL vers la description'), blank=True, null=True)
    """ The description URL of the document. """

    isbn = models.CharField(max_length=255, verbose_name=_('ISSN'), blank=True, null=True)
    """ The ISBN (International Standard Book Number) of the document. """

    isbn_num = models.CharField(
        max_length=255, verbose_name=_('ISSN numérique'), blank=True, null=True)
    """ The numeric ISBN (International Standard Book Number) of the document. """

    class Meta:
        ordering = ('title', )
        verbose_name = _("Document d'unité de recherche")
        verbose_name_plural = _("Documents d'unités de recherche")

    def __str__(self):
        return self.title


class SearchUnitDocumentAttachment(FedoraMixin, FedoraDated):
    """ A file attachment associated with a search unit document. """

    document = models.ForeignKey(
        SearchUnitDocument, related_name='attachments', verbose_name=_('Document'))
    """ The document associated with the file attachment. """

    file = models.FileField(verbose_name=_('Fichier'), upload_to='search_unit_attachments')
    """ The file of the attachment. """

    created = models.DateTimeField(
        auto_now_add=True, editable=False, verbose_name=_('Date de création'))
    """ The creation date of the attachment. """

    updated = models.DateTimeField(
        auto_now=True, editable=False, verbose_name=_('Date de modification'))
    """ The modification date of the attachment. """

    class Meta:
        verbose_name = _("Fichier de document d'une unité de recherche")
        verbose_name_plural = _("Fichiers de documents d'unités de recherche")

    def __str__(self):
        return '{} [{}]'.format(self.document, self.file)
