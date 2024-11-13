**Imperium**    
This application provides a simple, easy to navigate web interface for network mapping and simple penetration testing. It can be set up using docker and setting a few environment variables.   
Key feature of this application is its ability to install each of its components on different machines and connect them to the central controller. This is done by correctly setting all the endpoints. You can also choose, which components to install.

In the upper most directory of each component, eg. controller, scanner, ... you need to create a directory called instance. In this directory, create a file called config.py. In it you need to set the uri for the database. You can use any database you want, but Mysql or Mariadb is recommended, because the package needed to connect is already installed. You can install it on a container, vm or your local machine. You also need to create a database instance there, where the components can create and fill their tables. This is and example line in the config.py directory:

    DATABASE_URI = "mysql+pymysql://user:password@ip_address:port/database"

The rest of the configuration is done in the docker-compose.yml file. If you want to change the port the application runs on, you also need to change the port docker container exposes.

    ports:
        - your_port:your_port

Here are all the possible configurations. If an endpoint is left unset, it does not break the app, the particular component just wont be accessible.

    environment:
        RUNNING_PORT: "running_port"
        SCANNER_ENDPOINT: "scanner_endpoint"
