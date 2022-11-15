from setuptools import setup

test_deps = [
    'pytest', 
    'pytest-runner', 
    'pytest-cov', 
    'vcrpy', 
    'pytest-vcr', 
    'pytest-mock', 
    'requests-mock'
]

webpush_deps = [
    'http_ece>=1.0.5',
    'cryptography>=1.6.0',
]

blurhash_deps = [
    'blurhash>=1.1.4',
]

extras = {
    "test": test_deps + webpush_deps + blurhash_deps,
    "webpush": webpush_deps,
    "blurhash": blurhash_deps,
}

setup(name='Mastodon.py',
      version='1.6.1',
      description='Python wrapper for the Mastodon API',
      packages=['mastodon'],
      install_requires=[
          'requests>=2.4.2', 
          'python-dateutil', 
          'six', 
          'pytz',
          'python-magic',
          'decorator>=4.0.0', 
      ] + blurhash_deps,
      tests_require=test_deps,
      extras_require=extras,
      url='https://github.com/halcy/Mastodon.py',
      author='Lorenz Diener',
      author_email='lorenzd+mastodonpypypi@gmail.com',
      license='MIT',
      keywords='mastodon api microblogging',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Topic :: Communications',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
      ])
