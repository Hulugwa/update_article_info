from setuptools import setup, find_packages

setup(
    name='update_article_info',
    author='zhangxiang',
    version=None,
    include_package_data=True,
    packages=find_packages(),
    author_email='zzxxang@126.com',
    url=None,
    entry_points={
        'console_scripts': [
            'update-article-info = update_article_info.__init__:commandline'
        ]
    }
)