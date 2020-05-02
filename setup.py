from setuptools import setup

setup(name="thesaurus",
      version="0.1",
      description="Command line thesaurus",
      url="https://github.com/seddie95/Python_thesaurus",
      author="seddie95",
      licence="GPL3",
      install_requires=['pyspellchecker', 'bs4'],
      packages=['Python_thesaurus'],
      entry_points={
          'console_scripts': ['thesaurus=thesaurus_scripts.thesaurus:find_synonym',
                              'synonym=thesaurus_scripts.thesaurus:find_synonym']
      }
      )
