from setuptools import setup, find_packages

setup(
        name= 'miktools',
        version='0.0a1',
        description="Package containing general tools for daily stuff",
        author="Miquel Canyelles Niño",
        author_mail="mcanyellesnino@gmail.com",
        install_requires= ["numpy", "matplotlib"],
        url= "https://github.com/mikicanyelles/tools",
        packages= find_packages(),
        include_package_data=True
     )
