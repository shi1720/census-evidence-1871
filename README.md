# Census evidence, 1871

An executable documentary audit of a published institutional table in the 1871 census General Report for England and Wales, read alongside the 1861 and 1881 reports. The repository preserves historical descriptions as descriptions. It does not infer individual diagnoses or national prevalence.

## Reproduce

Python 3.9 or later; no third-party dependency is needed for the calculations or tests.

```sh
python3 analyze.py
python3 -m unittest -v
```

Optional figures:

```sh
python3 -m pip install -r requirements-figures.txt
python3 make_figures.py
```

`results/results.json` is generated deterministically. Figures are supplied as PNG and vector PDF. The unpublished manuscript is not included in this repository.

## Inputs

- `data/institutions_1871.csv`: all twelve rows of the institutional onset table, General Report (1873), p. lxii, note 27. Column totals: 665 recorded from birth, 389 “Others,” 1,054 total.
- `data/age_rates.csv`: seven age bands and four census years from the 1881 General Report (1883), pp. 63-64. Rates are per million people of the corresponding age, as enumerated and uncorrected.
- `data/source_tables.html`: the two attributed tables captured from A Vision of Britain. Header structure and original category wording are retained.
- `data/evidence.json`: eight selected extracts with source URLs; analytical selections, not an exhaustive corpus or independent observations.
- `data/source_manifest.json`: retrieval date and SHA-256 hashes of the full downloaded HTML. Only selected public-domain primary text is redistributed. Hashes identify the retrieved versions; they are not authenticity guarantees. A website's later HTML may differ.

Sources: [1861 report](https://www.visionofbritain.org/text/chap_page.jsp?c_id=11&cpub_id=EW1861GEN&t_id=SRC_P), [1871 report](https://www.visionofbritain.org/text/chap_page.jsp?c_id=6&cpub_id=EW1871GEN&t_id=SRC_P), [1881 report](https://www.visionofbritain.org/text/chap_page.jsp?c_id=10&cpub_id=EW1881GEN&t_id=SRC_P). Transcription service: University of Portsmouth, A Vision of Britain through Time. Accessed 16 October 2026.

Additional primary comparison: [Royal Commission appendix, 1889](https://www.niph.go.jp/toshokan/koten/Britain/PDF/100718700001.pdf), appendix 18, pp. 241-243; appendix 21, p. 254; appendix 27, p. 288. The 1881 counts and 37% statement were checked visually against appendix 18. The 1871 institutional table was checked for internal arithmetic, but not independently against a scan. The repository does not distribute the commission scan or secondary books.

## Results and interpretation

The pooled recorded-from-birth share is 63.09298%; its rounded complement is 37%. Institutional shares range from 41.55844% to 95.87629%. Omitting one institution at a time produces pooled shares from 59.77011% to 65.53911%. These are descriptive sensitivity checks, **not confidence intervals**.

The 1881 report replaces 498 enumerated children under five with 2,077 estimated children, yielding `13,295 - 498 + 2,077 = 14,874`. The added 1,579 is 11.87665% of the enumerated total. Rounded rates of 141 and 590 do not reproduce the estimated count exactly; the script uses the separately published counts.

The table's “Others” category is not automatically recoded to “acquired.” Completion scenarios deliberately vary the unresolved fraction of that category; these are logical illustrations, not observations of missingness. The 68-person difference between the institutional narrative total and onset-table total is not a fully reconciled set of identifiable records. Completion calculations over 1,122 are conditional on comparable coverage of those totals.

## Scope and prior work

This audit supports a narrow historical comparison: an institutional ratio and its use in the later report's national explanatory prose. It does not establish that the population actually had the same onset distribution. The reports' stated inclusion rules are evidence about published practice, not proof of every clerk's behaviour.

Closely relevant prior scholarship includes Kerstin Brückweh, *Menschen zählen* (2015), chapter IV; Sophie Ledebur, “Evidence of undercounting” (2021 issue, online 2023), DOI: 10.1017/S0269889723000078; Jennifer Esmail, *Reading Victorian Deafness* (2013); Graeme Gooday and Karen Sayer, *Managing the Experience of Hearing Loss in Britain, 1830-1930* (2017); and Coreen McGuire, *Measuring Difference, Numbering Normal* (2020). The general problem of census disability classification is established; the analysis does not claim to have discovered it.

## Rights

Original code: MIT license. Historical quotations and numerical tables are attributed public-domain primary material. The software license does not claim ownership over source editions, transcriptions, institutional names, or third-party website material. No personal resume, credentials, or unpublished manuscript is included.
