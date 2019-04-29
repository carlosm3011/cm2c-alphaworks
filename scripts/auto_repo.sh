#!/bin/bash

###################################################################
# auto repository manager helper script
#
# Scans current directory for all folders ending in ".git", changes
# into those folders and either runs git pull or git push
#
# 2019-03-18
###################################################################

REPOS=$(find . -type d -depth 1 -name "*git")

update()
{
	for repo in $REPOS
	do
		echo "%%% Updating $repo"
		cd $repo
		git pull
		cd ..
		echo
		echo
	done
}

push()
{
	for repo in $REPOS
	do
		echo "%%% Auto commit $repo"
		cd $repo
		if [ -f NOCOMMIT ]; then
			echo "Not committing or pushing $repo, NOCOMMIT exists"
		else
			git commit -a -m "auto commit"	
			echo "%%% Pushing $repo"
			git push
		fi
		cd ..
		echo
		echo
	done
}

CMD=$1

case $CMD in
	update)
		echo "CMD Updating all *.git repositories"
		echo
		update
		;;
	push)
		echo "CMD Pushing all *.git repositories"
		echo
		push
		;;
	*)
		echo "ERROR - Unknown command"
		echo "Usage ./auto_repo.sh update|push"
		;;
esac

