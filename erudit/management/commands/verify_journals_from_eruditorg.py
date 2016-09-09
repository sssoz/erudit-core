# -*- coding: utf-8 -*-

import os.path as op
from io import BytesIO
import re

from django.conf import settings
from django.core.management.base import BaseCommand
import requests
import lxml.etree as etree

from ...models import Journal

FIXTURE_ROOT = getattr(
    settings, 'JOURNAL_FIXTURES',
    op.join(op.dirname(__file__), 'fixtures')
)

SUPPORTED_LANGUAGES = [l[0] for l in settings.LANGUAGES]

def collection_from_logo(logo_url):
    if logo_url == '/revue/images/iconePersee2.gif':
        return 'Persée'
    elif logo_url == '/revue/images/iconeErudit2.gif':
        return 'Érudit'
    elif logo_url == '/revue/images/iconeUNB.gif':
        return 'UNB'
    elif logo_url == '/revue/images/iconeCNRC.gif':
        return 'NRC'
    else:
        return None


def journal_dict_from_xml(journal_html):
    """ Parse the legacy erudit.org html and returns a dict with the journal information """
    journal = {
        'collection': collection_from_logo(journal_html.find('img').get('src')),
    }

    # Check if the journal is active

    if journal_html.find('span[@class="titrepara"]') is not None:
        journal['title'] = journal_html.find('span').text
    elif journal_html.find('a') is not None:
        try:
            journal['title'] = journal_html.find('a').text.lower().strip()
        except:
            raise
        journal['link'] = journal_html.find('a').get('href')

        if journal['collection'] in ('Érudit', 'UNB',):
            try:
                journal['shortname'] = re.search("/revue/(\w+)", journal['link']).group(1)
            except Exception as e:
                raise
    else:
        pass
    return journal


class Command(BaseCommand):
    help = """Verify the integrity of the database against the eruditorg website"""

    def write_warning(self, string):
        self.stdout.write(self.style.WARNING(string))

    def write_failure(self, string):
        self.stdout.write(self.style.ERROR(string))

    def write_label(self, string):
        self.stdout.write(self.style.MIGRATE_LABEL(string))

    def write_success(self, string):
        self.stdout.write(self.style.SUCCESS(string))

    def fetch_scientific_journals_from_eruditorg(self):
        content = requests.get('http://www.erudit.org/revue/')

        xml_content = etree.parse(
            BytesIO(content.content),
            etree.HTMLParser(encoding='utf-8')
        )
        elements = xml_content.findall('//div[@id="corps"]/div[@id="contenu"]/ul[@class="listeRevue"]//li//p')  # noqa

        active_journals = []
        inactive_journals = []

        for element in elements:
            journal = journal_dict_from_xml(element)

            if element.find('span[@class="titrepara"]') is not None:
                inactive_journals.append(journal)
                continue
            else:
                active_journals.append(journal)
        return active_journals, inactive_journals

    def fetch_cultural_journals_from_eruditorg(self):
        webpage = requests.get('http://www.erudit.org/culture/')

        xml_content = etree.parse(
            BytesIO(webpage.content),
            etree.HTMLParser(encoding='utf-8')
        )
        elements = xml_content.findall('//ul[@class="listeRevue"]/li/p')

        active_journals = []
        for element in elements:
            if element.find('a') is not None:
                active_journals.append({
                    'title': element.find('a').text,
                    'localidentifier': re.match('/culture/(\w+)/', element.find('a').get('href')).group(1)
                })
        return active_journals

    def verify_unb_scientific_journals(self, journals):
        warning_count = 0
        self.write_label("Verify the UNB scientific journals")

        for journal in filter(lambda x: x['collection'] == 'UNB' and 'shortname' in x, journals):
            try:
                self.write_label("Verifying presence of {}".format(journal['shortname']))
                Journal.objects.get(code=journal['shortname'])
                self.write_success('  [OK]')
            except Exception as e:
                self.write_failure('  Journal "{}" is not present.'.format(journal['title']))
                self.write_failure("  [FAIL]")

    def verify_erudit_scientific_journals(self, journals):
        warning_count = 0
        self.write_label("Verify the Érudit scientific journals")

        for journal in filter(lambda x: x['collection'] == 'Érudit' and 'shortname' in x, journals):
            try:
                self.stdout.write(
                    self.style.MIGRATE_LABEL("Verifying presence of {}".format(
                        journal['shortname']
                    ))
                )

                jo = Journal.objects.get(code=journal['shortname'])

                def format_journal_name(journal):
                    if journal.subtitle:
                        return "{} : {}".format(
                            journal.name,
                            journal.subtitle
                        ).lower().strip()
                    return journal.name.lower().strip()

                if format_journal_name(jo) == journal['title']:
                       self.write_success('  [OK]')
                else:
                    warning_count += 1
                    self.stdout.write(self.style.WARNING('  [WARN] Name on legacy website is different than the name on the new website'))
                    self.stdout.write(self.style.MIGRATE_LABEL('    l: {}'.format(journal['title'])))
                    self.write_label('    n: {}'.format(format_journal_name(jo)))
            except:
                self.stdout.write(self.style.ERROR('  [FAIL] Journal "{}" is MISSING'.format(journal['title'])))
                raise
        if warning_count:
            self.write_warning("{} warnings".format(warning_count))

    def verify_erudit_cultural_journals(self, journals):
        warning_count = 0

        for journal in journals:
            try:
                self.write_label('Verifying presence of {}'.format(journal['title']))
                self.write_success('  [OK]')
            except:
                self.write_failure('  [FAIL]')


    def handle(self, *args, **options):
        self.stdout.write(
            self.style.MIGRATE_LABEL("Fetch scientific journals from eruditorg")
        )
        self.write_success('  [OK]')

        try:
            active_scientific_journals, inactive_scientific_journals = \
                self.fetch_scientific_journals_from_eruditorg()
        except Exception as e:
            self.stdout.write(
                self.style.ERROR("  [FAIL] Cannot fetch the journals from eruditorg: {}".format(e))
            )
            raise

        active_cultural_journals = self.fetch_cultural_journals_from_eruditorg()
        self.verify_erudit_scientific_journals(active_scientific_journals)
        self.verify_unb_scientific_journals(active_scientific_journals)
        self.verify_erudit_cultural_journals(active_cultural_journals)
