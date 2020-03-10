# AI Kegerator

This project uses [Greengo](https://github.com/rpedigoni/greengo) to manage Greengrass operations, in an automated, reliable, and repeatable way. You may read more about it [on this article](https://read.acloud.guru/aws-greengrass-the-missing-manual-2ac8df2fbdf4).


## Environment setup

Start creating a Python virtualenv running Python 2.7. *Python 3.x is not supported on Greengrass Lambda yet, so using version as default for the project.* The [virtualenvwrapper](http://virtualenvwrapper.readthedocs.io/en/latest/) lib is recommended to simplify management:

 mkvirtualenv aikegerator --python=python2.7

 If not already activated, do it by executing:

workon aikegerator

Then, install Greengo using `pip`:

    pip install git+git://github.com/rpedigoni/greengo.git#egg=greengo

We are currently using a fork which facilitates Greengrass groups to be redefined and also allows the usage of GGShadowService on subscriptions.

To mock the GPIO pins when deploying to non physical devices, we use GPIOCrust. There's been a number of updates to the repo but version pip points to doesn't have them. To fix this, install GPIOCrust doing this: 

	pip install git+https://github.com/zourtney/gpiocrust