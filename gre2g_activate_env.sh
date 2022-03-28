#!/bin/bash

conda activate gre2g

if [[ $(poetry config virtualenvs.create) == "true" ]]
then
  poetry_gre2g_env_path=$(poetry env list --full-path)
  if [[ $(echo $poetry_gre2g_env_path | grep Activated) ]]
  then
    source "$( echo $poetry_gre2g_env_path | grep Activated | cut -d' ' -f1 )/bin/activate"
  else
    source "$( echo $poetry_gre2g_env_path )/bin/activate"
  fi
fi