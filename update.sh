#!/bin/bash

function update {
    docker compose down --rmi --remove-orphans
    docker compose up -d
    docker image prune
}

case $1 in

    controller)
        cd controller
        update
        ;;
    
    scanner)
        cd scanner
        update
        ;;

    *)
        echo "such a tool does not exist"
        ;;

esac