
# Самые цитируемые патенты патентами, выпущенными в 1990 году в США.

lded   = LOAD '/data/patents/apat63_99.txt'  USING PigStorage(',');
apat   = FOREACH lded GENERATE (int) $0 AS patent, (int) $1 AS year, (chararray) $4 AS country;
cite   = LOAD '/data/patents/cite75_99.txt' USING PigStorage(',') AS (citing:int, cited:int);

ac     = JOIN apat BY patent, counts BY citing;
fac    = FILTER  ac BY    year ==   1990;
fapats = FILTER fac BY country == '"US"';

fgac   = FOREACH fac GENERATE citing AS citing, cited AS cited;
cited  = GROUP fgac BY cited;

counts = FOREACH cited GENERATE group AS cited, COUNT(cite) AS count;
result = JOIN  apat   BY patent, counts BY cited;
result = ORDER result BY count DESC;

STORE result INTO 'pig_res1';
STORE counts INTO 'pig_counts1';
STORE fapats INTO 'pig_apats1';

fresult = LIMIT result 10;
DUMP fresult;
