**Imperium**    
This application provides a simple, easy to navigate web interface for network mapping and simple penetration testing. It can be set up using docker and setting a few environment variables.   
Key feature of this application is its ability to install each of its components on different machines and connect them to the central controller. This is done by correctly setting all the endpoints. You can also choose, which components to install.

Deployment
---

In order to successfuly deploy this application, you need to have docker installed and have your user in the docker group. You can find out, how that is done, here: https://docs.docker.com/engine/install/                

You will also need the docker compose utility.

After you've successfuly installed docker, you can start the deploy.sh script in the upper most directory. If you provide no arguments to this script, it will give you the **help message**, which will display all the possible arguments. Note that each tool needs to be deployed with a different call to the deploy script. The deploy script accepts **only one argument**. You can use it for example like this:

```bash
./deploy.sh controller
./deploy.sh scanner
```

The deploy script will deploy a few containers, including a Mariadb one. There is also the option to not use the deploy script, if you want to. Some technical knowledge is needed for that tho.

The deploy script will also configure the connections to your database for you. If you deploy on more than one machine, you will need to modify the *instance/config.py* file yourself. This will be explained in the configuration phase

Configuration
---

In the upper most directory of each tool, the deploy script will create this file *instace/config.py*. In this file, you can find the URI for the controller database. The IP will be set to you machines ip by default and the port 3306, on which Mariadb will run. Note than this port will be tunneled from the container, so you mustn't have anything running on that port on your pc. Alternatively, you can change it in the docker compose script. The entry in *instance/config.py* will look like this:

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://user:password@ip_address:port/database"

The rest of the configuration is done in the docker-compose.yml file. If you want to change the port the application runs on, you also need to change the port docker container exposes.

    ports:
        - your_port:your_port

Here are all the possible configurations. If an endpoint is left unset, it does not break the app, the particular component just wont be accessible.

    environment:
        RUNNING_PORT: "running_port"
        SCANNER_ENDPOINT: "scanner_endpoint"

