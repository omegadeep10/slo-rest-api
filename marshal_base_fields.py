from flask_restful import fields

faculty_fields = {
	'faculty_id': fields.String,
    'email': fields.String,
	'first_name': fields.String,
	'last_name': fields.String,
    'user_type': fields.String
}

class_fields = {
    'crn': fields.String,
    'course_number': fields.String,
    'course_name': fields.String,
    'course_type': fields.String,
    'semester': fields.String,
    'course_year': fields.String(attribute=lambda x: x.course_year.year), # extract only the Year as a string
}

student_fields = {
	'student_id': fields.String,
	'first_name': fields.String,
	'last_name': fields.String
}

assigned_slo_fields = {
    'slo_id': fields.String,
    'slo_description': fields.String(attribute='slo.slo_description'),
    'comments': fields.String
}

slo_fields = {
	'slo_id': fields.String,
	'slo_description': fields.String
}

performance_indicator_fields = {
    'performance_indicator_id': fields.String,
    'performance_indicator_description': fields.String,
    'unsatisfactory_description': fields.String,
    'developing_description': fields.String,
    'satisfactory_description': fields.String,
    'exemplary_description': fields.String
}

score_fields = {
    'performance_indicator_id': fields.String,
    'score': fields.Integer
}