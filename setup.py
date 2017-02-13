from setuptools import setup, find_packages

setup(name='Mastodon.py',
      version='1.0.3',
      description='Python wrapper for the Mastodon API',
      packages=['mastodon'],
      install_requires=['requests', 'dateutils'],
      url='https://github.com/halcy/Mastodon.py',
      author='Lorenz Diener',
      author_email='lorenzd+mastodonpypypi@gmail.com',
      license='MIT',
      keywords='mastodon api microblogging',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Topic :: Communications',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
      ]
)
