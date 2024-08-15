#!/bin/bash

if [[ "$1" == "-h" || "$1" == "--help" ]]; then
  echo "Usage: $0 [tmux-session-name] [<-h|--help>]"
# if $1 is ls do tmux ls
elif [[ "$1" == "ls" ]]; then
  tmux ls
else 
  tmux attach -t $1 || tmux new -s $1
fi

