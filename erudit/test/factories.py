# -*- coding: utf-8 -*-

import datetime as dt

import factory
from faker import Factory

faker = Factory.create()


class OrganisationFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'organization{}'.format(n))

    class Meta:
        model = 'erudit.Organisation'


class PublisherFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'erudit.Publisher'


class CollectionFactory(factory.django.DjangoModelFactory):
    code = factory.Sequence(lambda n: 'journal-{}'.format(n))
    name = factory.Sequence(lambda n: 'Revue{}'.format(n))

    class Meta:
        model = 'erudit.Collection'


class DisciplineFactory(factory.django.DjangoModelFactory):
    code = factory.Sequence(lambda n: 'discipline-{}'.format(n))
    name = factory.Sequence(lambda n: 'Discipline{}'.format(n))

    class Meta:
        model = 'erudit.Discipline'


class JournalFactory(factory.django.DjangoModelFactory):
    code = factory.Sequence(lambda n: 'journal-{}'.format(n))
    name = factory.Sequence(lambda n: 'Revue{}'.format(n))
    localidentifier = factory.Sequence(lambda n: 'journal{}'.format(n))

    class Meta:
        model = 'erudit.journal'

    @factory.post_generation
    def publishers(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for group in extracted:
                self.publishers.add(group)


class JournalTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'erudit.JournalType'


class JournalInformationFactory(factory.django.DjangoModelFactory):
    journal = factory.SubFactory(JournalFactory)

    class Meta:
        model = 'erudit.journalinformation'


class IssueFactory(factory.django.DjangoModelFactory):
    journal = factory.SubFactory(JournalFactory)
    localidentifier = factory.Sequence(lambda n: 'issue{}'.format(n))
    date_published = dt.datetime.now().date()
    year = dt.datetime.now().year

    class Meta:
        model = 'erudit.issue'


class ArticleFactory(factory.django.DjangoModelFactory):
    issue = factory.SubFactory(IssueFactory)
    localidentifier = factory.Sequence(lambda n: 'article{}'.format(n))
    type = 'article'
    ordseq = 0

    class Meta:
        model = 'erudit.article'


class AuthorFactory(factory.django.DjangoModelFactory):
    lastname = faker.last_name()
    firstname = faker.first_name()

    class Meta:
        model = 'erudit.Author'


class ThesisFactory(factory.django.DjangoModelFactory):
    collection = factory.SubFactory(CollectionFactory)
    author = factory.SubFactory(AuthorFactory)
    title = factory.Sequence(lambda n: 'Thèse {}'.format(n))
    url = faker.url()
    publication_year = faker.year()

    class Meta:
        model = 'erudit.Thesis'


class SearchUnitFactory(factory.django.DjangoModelFactory):
    collection = factory.SubFactory(CollectionFactory)
    code = factory.Sequence(lambda n: 'journal-{}'.format(n))
    localidentifier = factory.Sequence(lambda n: 'journal-{}'.format(n))
    name = factory.Sequence(lambda n: 'Unité de recherche {}'.format(n))

    class Meta:
        model = 'erudit.SearchUnit'


class SearchUnitCollectionFactory(factory.django.DjangoModelFactory):
    search_unit = factory.SubFactory(SearchUnitFactory)
    localidentifier = factory.Sequence(lambda n: 'collection-{}'.format(n))
    title = factory.Sequence(lambda n: 'Collection {}'.format(n))

    class Meta:
        model = 'erudit.SearchUnitCollection'


class SearchUnitDocumentFactory(factory.django.DjangoModelFactory):
    collection = factory.SubFactory(SearchUnitCollectionFactory)
    localidentifier = factory.Sequence(lambda n: 'document-{}'.format(n))
    title = factory.Sequence(lambda n: 'Document {}'.format(n))
    abstract = factory.Sequence(lambda n: 'Abstract {}'.format(n))
    publication_year = faker.year()

    class Meta:
        model = 'erudit.SearchUnitDocument'
