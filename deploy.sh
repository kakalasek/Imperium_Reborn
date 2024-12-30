#!/bin/bash

#############################
# Help                      #
#############################

function help 
{
    echo "This is the list of possible tools to deploy"
    echo "Note that all but the first argument will be ignored"
    echo
    echo "Syntax: ./deploy [chosen option]"
    echo "options:"
    echo "controller    Deploys the main component of this program, the controller"
    echo "scanner       Deploys the scanner, it is used for network and host scanning"
}

#############################
# Create Config             #
#############################

function create_config
{
    MY_IP=`hostname -I | cut -d' ' -f1`

    echo "creating the instance folder"
    mkdir instance

    echo "creating the config.py file"
    touch instance/config.py

    echo "cofiguring database uri"
    echo "SQLALCHEMY_DATABASE_URI = \"mysql+pymysql://root:secret@$MY_IP:3306/imperium\"" > instance/config.py
}

#############################
# Controller Deploy         #
#############################

function deploy_controller
{
    cd controller

    create_config

    echo "composing containers"
    docker compose up -d

    echo "controller deployed"
}

#############################
# Scanner Deploy            #
#############################

function deploy_scanner
{
    cd scanner

    create_config

    echo "composing containers"
    docker compose up -d

    echo "scanner deployed"
}

#############################
# Main Program              #
#############################

if [ $# -eq 0 ]; then 
    help
else
    case $1 in

        controller)
            deploy_controller
            ;;

        scanner)
            deploy_scanner
            ;;
        
        *)
            echo "such a tool does not exist"
            ;;
    esac
fi