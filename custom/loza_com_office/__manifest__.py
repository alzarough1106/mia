# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    'name': "Loza Communication Office",
    'version': "1.0",
    'currency': 'LYD',
    'summary': "Loza Comunication Office Module",
    'category': "productivity",
    'sequence': "10",
    'description': """
A Module for Communication between areas Management
""",

    'depends': ['mail'],
    'data': [
        'data/sequence.xml',
        'security/groups.xml',
        'report/report_sample.xml',
        'views/loza_order.xml',
        'views/res_users.xml',
        'views/loza_office.xml',
        'views/loza_election_point.xml',
        'views/loza_order_response.xml',
        'views/loza_order_quest_response.xml',
        'views/loza_order_quest.xml',
        'security/ir.model.access.csv',
        'data/loza.office.csv',
        'data/loza.election.point.csv',
    ],
    'author': "Loza Inc",
    'website': "",
    'installable': True,
    'application': True,
    'auto_install': False,
}
