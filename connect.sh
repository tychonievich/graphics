#!/bin/bash

COURSE="$1"
TERM="$2"


case "$(uname)" in
    Darwin)
        DIR="/Volumes/$COURSE/$TERM/"
        MNT=(open "smb://courses.grainger.illinois.edu/$COURSE")
    ;;
    Linux)
        DIR="/run/user/$(id -u)/gvfs/smb-share:domain=UOFI,server=courses.grainger.illinois.edu,share=$COURSE,user=$USER/$TERM/"
        MNT=(gio mount "smb://UOFI;$USER@courses.grainger.illinois.edu/$COURSE")
        # uses gnome keyring by default, key for smb://$USER@courses.grainger.illinois.edu
        # try  seahorse  to edit this entry (GUI only)
        # try  gnome-keyring-daemon --unlock --replace  to unlock the keyring from the command line
    ;;
esac

if [ ! -d "$DIR" ]; then "${MNT[@]}"; fi
if [ -d "$DIR" ]; then echo "$DIR"; 
else echo "sftp.courses.grainger.illinois.edu:/courses/$COURSE/$TERM/"
fi
