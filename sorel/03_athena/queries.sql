-- Counts for tieouts
SELECT count(*) num_pe, sum(length) tot_size 
FROM PE_BIN

-- In binary, not in meta -- 0 rows
SELECT *
FROM pe_bin b
        left outer join pe_meta m
            on b.path = 's3://sorel-20m/09-DEC-2020/binaries/' || m.sha256
where m.sha256 is null
limit 1000

-- In meta, not in binaries, and is malware
SELECT *
FROM pe_meta m
        left outer join pe_bin b
            on b.path = 's3://sorel-20m/09-DEC-2020/binaries/' || m.sha256
where b.path is null
  and m.is_malware <> 0
limit 1000

-- Not in ember
SELECT count(*)     --43755 rows
FROM pe_meta m
        left outer join pe_bin b
            on b.path = 's3://sorel-20m/09-DEC-2020/binaries/' || m.sha256
        left outer join pe_missing_ember me
            on m.sha256 = me.sha256
where b.path is null
  and me.sha256 is null
  and m.is_malware <> 0
limit 1000

-- Find the largest PE
-- s3://sorel-20m/09-DEC-2020/binaries/cbc349a4c969295d945e0dad972bbcaeb10839889bbe36a8b66c7d49348fcffc 2020-12-03 05:31:52.000 937,282,029
-- Possible cause of crashing
select * from pe_bin where length =
(select max(length)
from pe_bin)