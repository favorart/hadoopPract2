echo off

set OUTPUT='PageRank_Step_'

type ..\pract2\%OUTPUT%0.txt | python mapper_hw2.py | sort | python reducer_hw2.py | sort > %OUTPUT%1.txt
echo %OUTPUT%0.txt

for /l %%i in (1,1,2) do (
	echo %OUTPUT%(%%i-1).txt
    type %OUTPUT%(%%i-1).txt | python mapper_hw2.py | sort | python reducer_hw2.py | sort > %OUTPUT%%%i.txt
	echo %OUTPUT%%%i.txt
)