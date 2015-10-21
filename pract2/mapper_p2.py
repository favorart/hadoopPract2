import sys

# mapper
for line in sys.stdin:
	if line.startswith('"'): continue
	print '\t'.join(line.strip().split(','))
