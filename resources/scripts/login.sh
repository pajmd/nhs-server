#!/usr/bin/env bash

# curl -data @login.txt -H 'Content-Type: application/json' http://192.168.1.4:5000/api/login
curl -d '{"email":"aaa@ddd.com","password":"cccccc","checked":[]}' -H 'Content-Type: application/json' http://192.168.1.4:5000/api/login
