# -*- coding: utf-8 -*-
{
    "name": "Medical Insurance Agency (HR)",
    "version": "1.0.0.0",
    "currency": 'LYD',
    "summary": "Medical Insurance Agency for Libya - Human Resources Customization",
    "category": "Industries",
    "description": """
    Developed and Maintained by Abr Afrikia Inc   
""",
    'sequence': "-190",
    "depends": ["hr","hr_holidays","hr_org_chart","hr_attendance","hr_contract","contacts","ow_web_responsive"],
    "data": [
        'data/org_chart.xml',
        'data/io.certification.csv',
        'data/tags.xml',
        'data/sequence.xml',
        'data/timeoff.xml',
        'data/actions.xml',
        'data/res_lang.xml',
        'data/res_state.xml',
        'views/hr_contract.xml',
        'views/employee_menu.xml',
        'wizard/loza_employee_transfer.xml',
        'data/activites.xml',
        'views/hr_employee.xml',
        'views/hr_attendance.xml',
        'views/io_exit_permissions.xml',
        'views/io_employment_degree.xml',
        'views/io_penalty.xml',
        'views/io_certification.xml',
        'data/res.xml',
        'security/groups.xml',
        'security/ir.model.access.csv',
    ],
    "author": "Abr Afrikia, Ltd. Libya",
    "website": "https://www.io.ly",
    "installable": True,
    "application": True,
    "auto_install": False,
    "images": ["static/description/Banner.png"],
}
