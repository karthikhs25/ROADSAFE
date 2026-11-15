ROADSAFE 3.0 - cleaned datasets

All data from user-uploaded MoRTH report and CSV files.
CSV files are separated by reporting grain: do not add totals from different tables together.
Monthly and road type data are NATIONAL totals, not state-wise.
Vehicle context values are rounded in thousands; do not treat them as exact counts.
Road-user categories describe victims killed, not the type of vehicle responsible.
Safety-device source has mislabeled rows; only combined totals were retained.
Use DATA_DICTIONARY.csv for file-level provenance.

QUALITY CHECKS:
- Monthly 2021 figures in report Table 7.2 sum to 412,632 accidents, but the report's printed annual total is 412,432 (difference 200). Original monthly entries have been preserved without silently changing them.
- State fatalities file has 35 nonblank state/UT entries for 2020 and 36 for other years; one 2020 value is missing in the source. National annual totals reconcile, but do not assume every state-year is present.
- Road type data from Table 2.3 is limited to 2021-2023; state-wise filters should not be applied to national totals.
