#!/bin/bash

docker build -t nall1994/servicoauth ./servicoAutorizacao
docker build -t nall1994servicoemail ./servicoEmail

docker-compose up