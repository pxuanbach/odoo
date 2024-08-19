{
    'name': "Hostel Management",
    'summary': "Manage Hostel easily",
    'description': "Efficiently manage the entire residential facility in the school.", # Supports reStructuredText(RST) format (description is Deprecated),
    'author': "Pham Xuan Bach",
    'website': "http://www.example.com",
    'category':  "Tools",
    'version': '17.0.1.0.0',
    'depends': ['base'],
    "data": [
        "security/hostel_security.xml",
        "security/ir.model.access.csv",
        "views/hostel.xml",
        "views/hostel_room.xml",
        "views/hostel_room_categ.xml",
        "views/hostel_student.xml",
        "views/hostel_amenities.xml",
        "views/hostel_categ.xml",
        "views/hostel_room_availability.xml",
        "views/res_config_settings.xml",
        "data/data.xml",
        'data/hostel_room_categ_data.xml',
        "wizard/assign_room_student.xml",
    ],
   'assets': {
        'web.assets_backend': [
            'my_hostel/static/src/scss/field_widget.scss',
            'my_hostel/static/src/js/field_widget.js',
            'my_hostel/static/src/xml/field_widget.xml',
        ],
    },
    'demo': [
        'data/hostel_data.xml', 
        'data/hostel_room_data.xml'
    ],
    "installable": True
}
