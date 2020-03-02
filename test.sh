#!/bin/bash

docker-compose run --rm airflow initdb

docker-compose run --rm airflow test conn s3_ok 2020-03-02
s3_ok=$?
docker-compose run --rm airflow test conn s3_fail 2020-03-02
s3_fail=$?
docker-compose run --rm airflow test conn s3_parse_fail 2020-03-02
s3_parse_fail=$?

docker-compose down -v

echo s3_ok $([[ $s3_ok -eq 0 ]] && echo -e "\e[32mok\e[39m" || echo -e "\e[31mfailed\e[39m")
echo s3_fail $([[ $s3_fail  -eq 0 ]] && echo -e "\e[32mok\e[39m" || echo -e "\e[31mfailed\e[39m")
echo s3_parse_fail $([[ $s3_parse_fail -eq 0 ]] && echo -e "\e[32mok\e[39m" || echo -e "\e[31mfailed\e[39m")
