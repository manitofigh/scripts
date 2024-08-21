#!/bin/bash

if [[ "$1" == "-h" || "$1" == "--help" ]]; then
  echo "Usage: $0 [tmux-session-name] [<-h|--help>]"
elif ! [[ -z "$2" ]]; then
  tmux rename-session -t $1 $2
elif [[ "$1" == "ls" || "$1" == "l" ]]; then
  tmux ls
elif ! [[ -z $(tmux ls | grep "$1") ]]; then
  tmux attach -t $1
# such session name already does not exist
else
  read -p "Create session '$1'? (y/n) " response;
  if [[ $response == "y" || $response == "Y" ]]; then
    tmux new-session -s "$1"
  else
    exit 1
  fi
fi
