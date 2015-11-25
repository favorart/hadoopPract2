
lded   = LOAD '/data/patents/apat63_99.txt'  USING PigStorage(',');
apat   = FOREACH lded GENERATE (int) $0 AS patent, (int) $1 AS gyear, (chararray) $4 AS country;
cite   = LOAD '/data/patents/cite75_99.txt' USING PigStorage(',') AS (citing:int, cited:int);

apat3  = FILTER   apat  BY (gyear == 1990) AND (country == '"US"');

cites  = JOIN     apat3   BY patent, cite BY citing;
citess = FOREACH  cites   GENERATE (int) $4 as cited, (int) $3 as citing;
groupd = GROUP    citess  BY cited;

counts  = FOREACH groupd  GENERATE group AS cited, COUNT(citess) AS cited_count;
counts  = ORDER   counts  BY cited_count DESC;

STORE counts INTO 'pig_result';

dump_counts = LIMIT  counts  10;
DUMP dump_counts;

