SELECT value, COUNT(*) AS n, MIN(from_unixtime(epoch)) AS first_seen
FROM "abt_aa_weesp_dydro_20261001_nonprod"."dydro_prep_pcs_string"
WHERE tag = -8801123487727717193
GROUP BY value
ORDER BY first_seen DESC
LIMIT 30
