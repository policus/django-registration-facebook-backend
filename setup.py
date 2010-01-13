from distutils.core import setup
import os

setup(name='django-registration-facebook-backend',
      version='0.1',
      description='Facebook Connect backend for django-registration',
      author='Joonas Bergius',
      author_email='joonas@policus.com',
      url='http://github.com/policusopensource/django-registration-facebook-backend/',
      packages=['facebook_connect', 'facebook_connect.templatetags'],
      package_data={'facebook_connect': ['templates/*.html'],}
     )