## How to configure a Compute Engine VM instance to serve requests

**How to make a Compute Engine instance to handle the request?**

1. Create a Compute Engine instance VM. Make sure it's in the same region as the cloud Function, and when creating it, allow HTTP connections to it. [Documentation](https://cloud.google.com/compute/docs/instances/create-start-instance#startinginstancewithimage). I used a `debian-9` image for this test.

2. SSH into the instance, and run the following commands:

- Install apache server

            sudo apt-get update
            sudo apt-get install apache2
            sudo apt-get install libapache2-mod-wsgi

- Install this python libraries as well:

            sudo apt-get install python-pip
            sudo pip install flask

3. Set up environment for your application:

        cd ~/
        mkdir app
        sudo ln -sT ~/app /var/www/html/app

Last line should point to the folder path where apache serves the index.html file from.

4. Create your app in `/home/<user_name>/app`:

**main.py**

    from flask import Flask, request
    app = Flask(__name__)
    
    @app.route('/', methods=['POST'])
    def receive_file():
        file_content = request.form['data']
        # TODO
        # Implement process to save this data onto a file
        return 'Hello from Flask!'
    
    if __name__ == '__main__':
      app.run()

5. Create wsgi server entrypoint, in the same directory:

**main.wsgi**

    import sys
    sys.path.insert(0, '/var/www/html/app')
    
    from main import app as application

6. Add the following line to `/etc/apache2/sites-enabled/000-default.conf`, after the `DocumentRoot` tag:

            WSGIDaemonProcess flaskapp threads=5
            WSGIScriptAlias / /var/www/html/app/main.wsgi
    
            <Directory app>
                    WSGIProcessGroup main
                    WSGIApplicationGroup %{GLOBAL}
                    Order deny,allow
                    Allow from all
            </Directory>

7. Run `sudo apachectl restart`. You should be able to send post requests to your application, to the internal IP of the VM instance (you can see it in the Console, in the Compute Engine section). Once you have it, in your cloud function, you should change the response line to:


        response = requests.post('<INTERNAL_INSTANCE_IP>/', headers=headers, data=data)

        return "Request sent to your instance with the data of the object"


