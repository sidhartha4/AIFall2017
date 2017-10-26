#!/bin/sh

g++ -Wall -O2 dumb.cpp 

./a.out < 1.1/7.txt > 1.1/dumb_sol_7.txt
./a.out < 1.1/8.txt > 1.1/dumb_sol_8.txt
./a.out < 1.1/9.txt > 1.1/dumb_sol_9.txt


g++ -Wall -O2 smart.cpp

./a.out < 1.1/7.txt > 1.1/smart_sol_7.txt
./a.out < 1.1/8.txt > 1.1/smart_sol_8.txt
./a.out < 1.1/9.txt > 1.1/smart_sol_9.txt
./a.out < 1.2/10.1.txt > 1.2/smart_10.1.txt
./a.out < 1.2/10.2.txt > 1.2/smart_10.2.txt


g++ -Wall -O2 smarter.cpp

./a.out < 1.1/7.txt > 1.1/sol_7.txt
./a.out < 1.1/8.txt > 1.1/sol_8.txt
./a.out < 1.1/9.txt > 1.1/sol_9.txt
./a.out < 1.2/10.1.txt > 1.2/sol_10.1.txt
./a.out < 1.2/10.2.txt > 1.2/sol_10.2.txt
./a.out < ec/12x12.txt > ec/sol_12x12.txt
./a.out < ec/12x14.txt > ec/sol_12x14.txt
./a.out < ec/14x14.txt > ec/sol_14x14.txt
