# Legal and historical sources for the IAP review

`MANIFEST.tsv` in this folder, and the one in `../law/`, lists every source the checks in `reports/iap_review/claims_graded.md` rely on. For each source it gives the filename, the URL, the retrieval time (MST, 2026-11-02, approximate to the minute) and the SHA-256. The last column, `committed`, says whether the file is in this folder (`yes`) or is recorded by URL and hash only (`no (hash only)`): 11 of the 28 rows in `law/` and 10 of the 24 in `web/` are hash only, so those 21 hashes can be checked only by fetching the URL. The `web/` manifest has no header row; its columns are the same six, in the same order.

**Committed here:** official documents. These are from governments, legislatures, courts, Statistics Canada, Elections Alberta, municipalities and Indigenous Services Canada.

**Recorded only by URL and SHA-256, not committed:** news articles, commentary and other third-party pages. These include CityNews, CP24, BetaKit, BNN Bloomberg, ReNew Canada, Macdonald-Laurier Institute, Substack, Wikipedia, Mondaq, CBC, Grand Forks Gazette, National Newswatch, Choose Lethbridge and Medicine Hat Insights. They are not ours to republish. The audit keeps local copies, and a reader can fetch the URL and compare the hash. Pages built on each request may not match byte for byte.

Some sites (Cloudflare-protected) blocked automated download. Claims that rest on pages read without archiving are flagged in `claims_graded.md`.
