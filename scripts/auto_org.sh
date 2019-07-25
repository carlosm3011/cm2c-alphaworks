#!/bin/bash

cat << EOF 

Auto-Management of GitHub Orgs

(c) CarlosM, carlos@xt6labs.io

EOF


# variables

ORG="cm2c-internet-measurements"
GITHUB_AT="e6c272bab02a0214a87de3a8339b1ed791c34dea"

echo Cloning all repos for ORG=$ORG

mkdir -p $ORG
cd $ORG

repos=$(curl -s https://$GITHUB_AT:@api.github.com/orgs/$ORG/repos?per_page=200 | jq .[].clone_url | tr -d \" )

for r in $repos
do

    echo Cloning repo=$r
    git clone $r
done

