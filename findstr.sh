# grep script to isolate strings that might have an issue

# TODO remove ones that only have integer and no f' or f"

# searches for all strings in {  } and isolates those where there is no f"
grep -Er "\{[A-Za-z0-9_]+}" *.py | grep -v "f'" | grep -v 'f"' *.py
