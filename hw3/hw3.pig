
# pig -x local
# pig -Dmapred.job.queue.name=default

# Необходимо посчитать наиболее часто цитируемые в 1990 году патенты в США.
lded = LOAD '/data/patents/apat63_99.txt'  USING PigStorage(',');
apat = FOREACH lded GENERATE (long) $0 AS patent, (int) $1 AS year, (chararray) $4 AS country;
cite = LOAD '/data/patents/cite75_99.txt' USING PigStorage(',') AS (citing:int, cited:int);

cited  = GROUP cite BY citing;
counts = FOREACH cited GENERATE group AS citing, COUNT(cite) AS count;

fapats = FILTER  apat  BY country == '"US"';
fapats = FILTER fapats BY year    == 1990;

result = JOIN  fapats BY patent, counts BY citing;
result = ORDER result BY count DESC;
STORE result INTO 'pig_res';

result = LIMIT result 10;
DUMP result;



# lded = LOAD 'apat.txt' USING PigStorage(',');
# cite = LOAD 'cite.txt' USING PigStorage(',') AS (citing:int, cited:int);
