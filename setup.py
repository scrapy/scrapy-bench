from setuptools import setup


setup(
    name='Scrapy-Benchmark',
    version='1.0',
    py_modules=['scrapy-bench'],
    install_requires=[
        'Click',
        'scrapy',
        'statistics',
        'six',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'scrapy-bench=bench:cli',
        ]
    }
)
