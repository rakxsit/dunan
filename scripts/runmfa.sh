#!/bin/bash

# Use this script to recursively align files within folders
# Usage: bash runmfa.sh

for f in *; do

	# If it is a directory
	if [ -d "$f" ]; then

		echo "$f"

		/opt/montreal-forced-aligner/bin/mfa_validate_dataset "$f/unaligned" "$f/dictionary.txt"
		/opt/montreal-forced-aligner/bin/mfa_align "$f/unaligned" "$f/dictionary.txt" "english" "$f/aligned"

	fi

done