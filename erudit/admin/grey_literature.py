# -*- coding: utf-8 -*-

from django.contrib import admin

from ..models import SearchUnit
from ..models import SearchUnitCollection
from ..models import SearchUnitDocument
from ..models import SearchUnitDocumentAttachment


class SearchUnitAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'localidentifier', 'code', 'name', 'subname', )
    list_display_links = ('__str__', 'localidentifier', 'code', 'name', )


class SearchUnitCollectionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'localidentifier', 'search_unit', )
    list_display_links = ('__str__', 'localidentifier', )
    raw_id_fields = ('search_unit', )


class SearchUnitDocumentAttachmentInline(admin.TabularInline):
    extra = 0
    model = SearchUnitDocumentAttachment


class SearchUnitDocumentAdmin(admin.ModelAdmin):
    inlines = (SearchUnitDocumentAttachmentInline, )
    list_display = ('__str__', 'localidentifier', 'collection', )
    list_display_links = ('__str__', 'localidentifier', )
    raw_id_fields = ('collection', 'authors', 'publisher', )


class SearchUnitDocumentAttachmentAdmin(admin.ModelAdmin):
    list_display = ('__str__', )
    list_display_links = ('__str__', )


admin.site.register(SearchUnit, SearchUnitAdmin)
admin.site.register(SearchUnitCollection, SearchUnitCollectionAdmin)
admin.site.register(SearchUnitDocument, SearchUnitDocumentAdmin)
admin.site.register(SearchUnitDocumentAttachment, SearchUnitDocumentAttachmentAdmin)
