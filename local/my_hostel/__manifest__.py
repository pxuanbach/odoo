{
    'name': "Hostel Management",
    'summary': "Manage Hostel easily",
    'description': "Efficiently manage the entire residential facility in the school.", # Supports reStructuredText(RST) format (description is Deprecated),
    'author': "Pham Xuan Bach",
    'website': "http://www.example.com",
    'category': 'Uncategorized',
    'version': '17.0.1.0.0',
    'depends': ['base'],
    "data": [
        "security/hostel_security.xml",
        "security/ir.model.access.csv",
        "views/hostel.xml",
    ],
    # 'assets': {
    # 	'web.assets_backend': [
    #     	'web/static/src/xml/**/*',
    # 	],
    # },
    # 'demo': ['demo.xml'],
}
