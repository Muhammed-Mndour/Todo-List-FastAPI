#!/bin/bash

sub_help() {
	printf "${yel}List of all available commands:${end}\n\n"
	declare -F | grep sub | awk '{print $3}' | cut -c 5- | awk '{print " * " $0}' | awk 'length($0)>4'
}

get_app_name() {
	echo $(yq '.services.app.container_name' docker-compose.yml)
}

sub_up() {
	echo -e "${yel} Running docker-compose up...${end}"
	docker-compose up -w --build --force-recreate --remove-orphans
}

sub_down() {
	echo -e "${yel} Running docker-compose down...${end}"
	docker-compose down
}

sub_test() {
	echo -e "${yel}Running tests...${end}"
	sub_exec pytest -v $@
}

sub_t() {
	sub_test $@
}

sub_in() {
	echo -e "${yel} Diving inside app container...${end}"
	docker exec -it $(get_app_name) bash
}


sub_exec() {
	echo -e "${yel}Executing command $1 inside container...${end}"
	docker exec -it $(get_app_name) $@
}

sub_x() {
	sub_exec $@
}

red=$'\e[1;31m'
grn=$'\e[1;32m'
yel=$'\e[1;33m'
end=$'\e[0m'

subcommand=$1
case $subcommand in
"" | "-h" | "--help")
	sub_help
	;;
*)
	shift
	arr=($(declare -F | grep sub | awk '{print $3}' | cut -c 5-))
	if [[ ! " ${arr[@]} " =~ " ${subcommand} " ]]; then
		echo "${red}Error: '$subcommand' is not a known subcommand.${end}"
		echo "       ${yel}Run '$ProgName --help' for a list of known subcommands.${yel}"
		exit 1
	fi
	sub_${subcommand} $@
	;;
esac
