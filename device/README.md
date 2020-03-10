# AI Kegerator

This project uses [Greengo](https://github.com/rpedigoni/greengo) to manage Greengrass operations, in an automated, reliable, and repeatable way. You may read more about it [on this article](https://read.acloud.guru/aws-greengrass-the-missing-manual-2ac8df2fbdf4).

At the time of writing this, AWS CloudFormation didn't support Greengrass so I used Greengo as an alternative. 


## Environment setup
Note, when I wrote this, Greengrass didn't support python 3.x so I wrote it in Python 2.7. If I have time I'll upgrade it. 

Start creating a Python virtualenv running Python 2.7. *Python 3.x is not supported on Greengrass Lambda yet, so using version as default for the project.* The [virtualenvwrapper](http://virtualenvwrapper.readthedocs.io/en/latest/) lib is recommended to simplify management:

 mkvirtualenv aikegerator --python=python2.7

 If not already activated, do it by executing:

workon aikegerator

Then, install Greengo using `pip`:

    pip install greengo

To mock the GPIO pins when deploying to non physical devices, we use GPIOCrust. There's been a number of updates to the repo but version pip points to doesn't have them. To fix this, install GPIOCrust doing this: 

	pip install git+https://github.com/zourtney/gpiocrust
