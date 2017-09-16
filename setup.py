from distutils.core import setup

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()
    raise SystemError('Not about to address .md file.')

setup(
  name = 'guitarHarmony',
  packages = ['guitarHarmony'], # this must be the same as the name above
  version = '0.3',
  description = 'A python wrapper to learn music theory in Guitar.',
  long_description = long_description,
  author = 'Xi He',
  author_email = 'heeryerate@gmail.com',
  url = 'https://bitbucket.org/Xi_He/music-theory', # use the URL to the github repo
  download_url = 'https://bitbucket.org/Xi_He/music-theory/get/0.3.zip', # I'll explain this in a second
  keywords = ['music', 'theory', 'guitar', 'harmony'], # arbitrary keywords
  classifiers = [],
)
