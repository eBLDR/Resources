# Make - utility to maintain groups of programs
# Makefile is make's config file
# <command> take bash commands

# <alias_1>
#   <command_1>
#   ...
#   <command_n>

# <alias_2>
#   <command_1>
#   ...
#   <command_n>

# Defalt goal can be specified
.DEFAULT_GOAL := say-hi

say-hi:
	echo hi

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
