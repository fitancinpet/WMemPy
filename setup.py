from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = ''.join(f.readlines())

setup(
    name='wmempy',
    version='0.1.0',
    description='Windows Process Wrapper',
    long_description=long_description,
    author='Petr Ančinec',
    author_email='ancinpet@fit.cvut.cz',
    keywords='github,click,winapi,readprocessmemory,writeprocessmemory,openprocess,aob,scan',
    license='MIT License',
    url='https://github.com/fitancinpet/WMemPy',
    packages=find_packages(include=['committee', 'committee.*']),
    install_requires=['pywin32', 'numpy==1.19.3', 'click>=6'],
    python_requires='>=3.7',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Environment :: Console',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: Microsoft',
        'Topic :: Software Development :: Libraries'
    ],
    entry_points={
        'console_scripts': [
            'committee=committee.committee:main',
        ],
    },
    zip_safe=False,
    package_data={'committee': ['templates/*.html']},
)