# Websocket & Chart with Angular 17 and Fastapi (fake data in ML)

We create data for a model Machine Learning to send it to the client in Angular 17 with websocket in streaming.
- Angular 17, fastapi and postgres with no ORM's

## Back

### virtual environment
- A database must be created in postgres
* $ sudo su - postgres
* $ psql
* $ CREATE USER db WITH password 'db';
* $ CREATE DATABASE db WITH OWNER db;

* $ virtualenv entorno_virtual -p python3.11
* $ source entorno_virtual/bin/activate
* $ pip install -r requirements.txt

- we can create tables and insert data with differents environments in VSC, have a look at see file "launch.json"

## Others interesting commands
- $ sudo apt-get update
- $ sudo apt-get install libpq-dev

## Front 

### Angular 17
- sin fichero app.module.ts - modo standalone, luego hay que meter otros modulos generales en app.config.ts
* $ npx -p @angular/cli@17.0.0 ng new front

- con fichero app.module.ts
* $ npx -p @angular/cli@17.0.0 ng new front --no-standalone
* style: scss

* $ ng new my-app --no-standalone --routing --ssr=false

- component home
* $ npx ng g component components/home

## run front
$ npx ng serve

## install socketio
* $ npm install socket.io

## services
-create folder app/services/
services/$ npx ng generate service websocket

* $ npm install @swimlane/ngx-charts --save
* $ npm i @swimlane/ngx-charts
- declaration for ts
* $ npm install --save-dev @types/d3-shape
* $ npm install --save-dev @types/d3-scale
* $ npm install --save-dev @types/d3-shape
* $ npm install --save-dev @types/d3-selection
