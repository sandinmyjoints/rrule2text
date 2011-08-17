from distutils.core import setup

setup(name='rrule2text',
      version=__import__(rrule2text).get_version().replace(' ', '-'),
      author="William Bert",
      author_email="william.bert@gmail.com",
      py_modules=['rrule2text'],
      )