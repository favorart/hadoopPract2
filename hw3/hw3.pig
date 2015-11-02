
# Самые цитируемые патенты 1990го года США.

lded   = LOAD '/data/patents/apat63_99.txt'  USING PigStorage(',');
apat   = FOREACH lded GENERATE (int) $0 AS patent, (int) $1 AS year, (chararray) $4 AS country;
cite   = LOAD '/data/patents/cite75_99.txt' USING PigStorage(',') AS (citing:int, cited:int);

cited  = GROUP cite BY cited;
counts = FOREACH cited GENERATE group AS cited, COUNT(cite) AS count;

fapats = FILTER  apat  BY country == '"US"';
fapats = FILTER fapats BY year    == 1990;
result = JOIN  fapats BY patent, counts BY cited;
result = ORDER result BY count DESC;

STORE result INTO 'pig_res';
STORE counts INTO 'pig_counts';
STORE fapats INTO 'pig_apats';

fresult = LIMIT result 10;
DUMP fresult;


# pig -x local
# pig -Dmapred.job.queue.name=default

# counts = LOAD 'pig_counts' AS (cited:int, count:int);
# fapats = LOAD 'pig_apats'  AS (patent:int, year:int, country:chararray);
# result = LOAD 'pig_res'    AS (patent:int, year:int, country:chararray, cited:int, count:int);

# lded = LOAD 'apat.txt' USING PigStorage(',');
# cite = LOAD 'cite.txt' USING PigStorage(',') AS (citing:int, cited:int);
