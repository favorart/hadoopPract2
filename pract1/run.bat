@echo off

setlocal enabledelayedexpansion

set OUTPUT=text
set EXT=.txt

echo test.txt
type test.txt | python mapper_p1.py | sort | python reducer_p1.py | sort > %OUTPUT%0%EXT%
echo %OUTPUT%0%EXT%

for /L %%i in (1,1,2) do (
	set /A y=%%i-1

	rem echo %OUTPUT%!y!%EXT%
	type %OUTPUT%!y!%EXT% | python mapper_p1.py | sort | python reducer_p1.py | sort > %OUTPUT%%%i%EXT%
	echo %OUTPUT%%%i%EXT%
)

endlocal