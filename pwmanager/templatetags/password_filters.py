from ..models import Password
from django.utils import timezone
from django import template
import re
register = template.Library()
@register.filter
def age(p):
	return timezone.now() - p.date_created

@register.filter
def description(p):
	desc = '{} chatacter{}, consist of '.format(len(p),'' if len(p) == 1 else 's')
	attr = []
	if re.search('[a-z]',p): attr.append('lowercase letters')
	if re.search('[A-Z]',p): attr.append('uppercase letters')
	if re.search('[0-9]',p): attr.append('numbers')
	if re.search('[!@#$%^&*()\{\}\\;\'\"\[\],./<>?]',p): attr.append('punctuations')
	desc += ', '.join(attr)
	return desc

def json_friendly(pw):
	pw['date_created'] = str(timezone.now() - pw['date_created']).split(',')[0]
	pw['description'] = description(pw['password'])
	return pw