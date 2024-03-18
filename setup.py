from setuptools import find_packages,setup

setup(
    name="mcqgenerator", # name of the package
    version="0.0.1",     #version
    author="karuppasamy", #autor
    author_email="karuppasamy.v@igtsolutions.com", # email
    install_requires=['openai','langchain','streamlit','python-dotenv','PyPDF2'],
    packages=find_packages()

)


#-e . inside requirment.txt it will setup our current folder __init__.py learn more gothorugh internet
 
# we can directly install in this current folder by using cmd in terminal 
# python setup.py install i am not sure this is right or wrong check it once
# run cmd pip install -r requirements.txt it will install all lib

# when i run first reuirements.txt file i got one error in langchain lib
# i have installed separatly for that then i run the same  file it wasnt install without any error the new one folder was created name as mcqgeneratoe.egg.info