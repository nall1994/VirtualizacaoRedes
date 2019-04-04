#!/bin/bash

docker build -t bruno/servicoauth ./servicoAutorizacao
docker build -t bruno/servicoemail ./servicoEmail

docker-compose up