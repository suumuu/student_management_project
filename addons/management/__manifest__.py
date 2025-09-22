{
    'name': 'Student Management',
    'version': '1.1',
    'summary': 'Manage students and courses with validations',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'data/predefined_courses.xml',
        'views/student_views.xml',
        'views/course_views.xml',
        'report/student_course_report.xml',
       
    ],
    'installable': True,
    'application': True,
} 

