from setuptools import setup

setup(
        name='Scrapy-Benchmark',
        version='1.0',
        packages=['scrapy_bench'],
        install_requires=[
            'Click',
            'scrapy',
            'statistics',
            'six',
            'vmprof',
            'colorama<=0.4.1',
        ],
        entry_points='''
		[console_scripts]
		scrapy-bench=bench:cli
		''',
)
