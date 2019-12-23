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

say-hi:
	echo hi

help:
	man make

# Recursive invocation of make itself
say-hi-again:
	$(MAKE) say-hi

# The value of this variable is the file name with which make was invoked
