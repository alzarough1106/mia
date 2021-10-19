# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    'name': "Loza Media Office",
    'version': "1.0",
    'currency': 'LYD',
    'summary': "Election Media Office Module",
    'category': "productivity",
    'sequence': "-111",
    'description': """
A Module for arranging media events between areas Management
""",

    'depends': ['mail'],
    'data': [
        'data/sequence.xml',
        'views/loza_event.xml',
#        'security/groups.xml',
        'views/loza_office.xml',
        'views/loza_election_point.xml',
        'views/loza_event_response.xml',
        'views/loza_event_quest.xml',
        'security/ir.model.access.csv',
    ],
    'author': "Loza Inc",
    'website': "",
    'installable': True,
    'application': True,
    'auto_install': False,
}
