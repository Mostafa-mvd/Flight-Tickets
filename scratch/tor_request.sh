#!/bin/bash


echo -e "Tor controller port is running?\n"
sudo netstat -plnt | grep 9051;

echo -e "Killing all tor processes\n"
sudo killall tor;

echo -e "Restarting tor process for accessing tor control port\n"
sudo service tor stop;
sudo service tor start;
sudo service tor restart;

while :; do
	echo -e "Setting new tor ip address\n"
	echo -e 'AUTHENTICATE "SigmaZ2015"\r\nsignal NEWNYM\r\nQUIT' | nc 127.0.0.1 9051;
	sleep 3;
	echo -e "\n";
	sudo torify curl "http://icanhazip.com/";
	echo -e "\n---";
	sleep 2;
done
