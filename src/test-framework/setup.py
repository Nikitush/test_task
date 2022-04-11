from setuptools import setup, find_packages


with open('requirements.txt', 'r') as file:
    install_requires = file.readlines()


setup(
    name='framework',
    version='1.0',
    author='Nikita Goncharov',
    author_email='071299nik@mail.ru',
    description='Test framework for test task',
    python_requires='>=3.7',
    install_requires=install_requires,
    packages=find_packages()
)
