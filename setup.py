from setuptools import setup

test_deps = ['pytest', 'pytest-cov', 'vcrpy', 'pytest-vcr', 'pytest-mock']
extras = {
      "test": test_deps
}

setup(name='Mastodon.py',
      version='1.2.2',
      description='Python wrapper for the Mastodon API',
      packages=['mastodon'],
      setup_requires=['pytest-runner'],
      install_requires=['requests', 'python-dateutil', 'six', 'pytz', 'decorator'],
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
