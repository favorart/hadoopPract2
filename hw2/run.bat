@echo off

setlocal enabledelayedexpansion

set OUTPUT=text
set EXT=.txt

rem echo test.txt
echo ..\pract2\cite75_99.txt
type ..\pract2\cite75_99.txt | python mapper_hw2.py | sort | python reducer_hw2.py | sort > %OUTPUT%0%EXT%
echo %OUTPUT%0%EXT%

for /L %%i in (1,1,30) do (
	set /A y=%%i-1

	rem echo %OUTPUT%!y!%EXT%
	type %OUTPUT%!y!%EXT% | python mapper_hw2.py | sort | python reducer_hw2.py | sort > %OUTPUT%%%i%EXT%
	echo %OUTPUT%%%i%EXT%
)

endlocal