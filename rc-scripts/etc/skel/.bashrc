# /etc/skel/.bashrc:
# This file is sourced by all *interactive* bash shells on startup,
# including some apparently interactive shells such as scp and rcp
# that can't tolerate any output.

source /etc/profile

# Test for an interactive shell.  There is no need to set anything
# past this point for scp and rcp, and it's important to refrain from
# outputting anything in those cases.
if [[ $- != *i* ]]; then
	# Shell is non-interactive.  Be done now
	return
fi

# Shell is interactive.  It is okay to produce output at this point,
# though this example doesn't produce any.  Do setup for
# command-line interactivity.

# colors for ls, etc.  Prefer ~/.dir_colors #64489
if [[ -f ~/.dir_colors ]]; then
	eval `dircolors -b ~/.dir_colors`
else
	eval `dircolors -b /etc/DIR_COLORS`
fi

alias d="ls --color"
alias dir="ls --color"
alias ls="ls --color=auto"
alias ll="ls --color -l"
alias la="ls --color -la"
alias cls="clear"
alias cd..="cd .."
alias rm="rm -i"
alias mv="mv -i"
alias cp="cp -i"


# Change the window title of X terminals 
case $TERM in
	xterm*|rxvt|Eterm|eterm)
		PROMPT_COMMAND='echo -ne "\033]0;${USER}@${HOSTNAME%%.*}:${PWD/$HOME/~}\007"'
		;;
	screen)
		PROMPT_COMMAND='echo -ne "\033_${USER}@${HOSTNAME%%.*}:${PWD/$HOME/~}\033\\"'
		;;
esac

[ -f /etc/profile.d/bash-completion ] && source /etc/profile.d/bash-completion
[ -f /etc/profile.d/mc ] && source /etc/profile.d/mc

if [ "$EUID" = 0 ] || [ "`/bin/whoami`" = 'root' ]; then
	export PS1='\[\033[01;32m\]\u@\h \[\033[01;33m\]\W \$ \[\033[00m\]'
else
	export PS1='\[\033[01;31m\]\h \[\033[01;34m\]\W \$ \[\033[00m\]'
fi

export GTK2_RC_FILES=$HOME/.gtkrc-2.0

