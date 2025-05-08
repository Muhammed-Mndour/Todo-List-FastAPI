#!/bin/bash

sub_help() {
	printf "${yel}List of all available commands:${end}\n\n"
	declare -F | grep sub | awk '{print $3}' | cut -c 5- | awk '{print " * " $0}' | awk 'length($0)>4'
}

get_container_name() {
  path=$(yq '.include[0].path' docker-compose.yml)
	service=$(yq '.services|keys|.[0]' ${path})
	container_name=$(docker-compose ps ${service} --format "{{.Names}}")
	container_id=$(docker-compose ps ${service} -q)

  if [[ -z "${container_name}" ]]; then
    echo -e "${red}Error: No running container found for service '${service}'.${end}"
    echo -e "${yel}Make sure to start the containers with 'dev up' first.${end}"
    exit 1
  fi

  echo ${container_name}
}

sub_env_up() {
	echo -e "${yel} Running env docker-compose up...${end}"
	docker-compose -f ./dev-env/docker-compose.yml up -w --build --force-recreate --remove-orphans
}

sub_up() {
  if [[ "$1" == "--env" ]]; then
    sub_env_up
  else
  	echo -e "${yel} Running docker-compose up...${end}"
	  docker-compose up -w --build --force-recreate --remove-orphans
  fi
}

sub_env_down() {
  echo -e "${yel} Running env docker-compose down...${end}"
  docker-compose -f ./dev-env/docker-compose.yml down
}

sub_down() {
  if [[ "$1" == "--env" ]]; then
    sub_env_down
  else
  	echo -e "${yel} Running docker-compose down...${end}"
	  docker-compose down
  fi
}

sub_test() {
	echo -e "${yel}Running tests...${end}"
	sub_exec pytest -v $@
}

sub_t() {
	sub_test $@
}

sub_in() {
  container_name=$(get_container_name)
	echo -e "${yel} Diving inside app container ${container_name}...${end}"
	docker exec -it ${container_name} bash
}

sub_exec() {
  container_name=$(get_container_name)
	echo -e "${yel}Executing command \"$@\" inside container ${container_name}...${end}"
	docker exec -it ${container_name} $@
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
