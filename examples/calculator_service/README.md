# Calculator Service demo

This is a really simple/dummy service which implements a calculator with Servant.  There is a
Docker file which can make it easier to get up and running.  To run this:

```
$ ./build.sh
$ docker run -it --rm  servant/calculator bash
root@557b6ba4e2c9:/code# python test_calculator.py 
100.0 / 6.0 = 16.6666666667
```

It's also possible to mount the current working directory as a volume so that you can hack on the
`test_calculator.py` script

```
docker run -it --rm -v `pwd`:/code  servant/calculator bash
```

Now you can edit any files on your host system and that is reflected in the Docker container automatically.

In this default configuration, service calls are executed as a local Python library call.  In order to execute the service calls over HTTP, stand up the uwsgi http server:

```
docker run -it --rm -v `pwd`:/code -p 8888:8888 servant/calculator uwsgi --ini uwsgi.ini
```

Now, from your host system, uncomment the `client.configure()` line in `test_calculator.py`, update the host and port (which is 8888 in our example above) and launch `test_calculator.py` from your host system.  You should get the exact same response and see uwsgi reply to the request.
