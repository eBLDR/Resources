# Make - utility to maintain groups of programs
# Makefile is make's config file

# Makefile consists of a set of rules. A rule generally looks like:

# targets : dependent
#    command
#    command
#    command

# Targets are file names, separated by spaces. Typically,
# there is only one per rule.

# The commands are a series of steps typically used to make the target(s).
# These are bash commands, and need to start with a tab character, not spaces.

# The prerequisites are also file names, separated by spaces. These
# files need to exist before the commands for the target are run.

# make program allows you to use macros, which are similar to variables.
# Macros are defined in a Makefile as = pairs.
MACROS  = ":*)"

# Default goal can be specified
.DEFAULT_GOAL := say-hi

say-hi:
	echo hi

	# To avoid echoing the echo
	@echo hi

help:
	man make

# Recursive invocation of make itself
say-hi-again:
	$(MAKE) say-hi

# The value of this variable is the file name with which make was invoked

# Variables can be created
MY_VAR := whatsup

# And called
var:
	echo $(MY_VAR)
