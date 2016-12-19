 [ "table.py" -nt "docs/table.html" ] && pycco table.py
zip -qu docs/zips/table.zip docs/table.html docs/pycco.css table.py num.py GLOBALS.py opt.py sym.py
git add docs/* docs/zips/*

 [ "csv.py" -nt "docs/csv.html" ] && pycco csv.py
zip -qu docs/zips/csv.zip docs/csv.html docs/pycco.css csv.py
git add docs/* docs/zips/*

 [ "cliffsDeltaeg.py" -nt "docs/cliffsDeltaeg.html" ] && pycco cliffsDeltaeg.py
zip -qu docs/zips/cliffsDeltaeg.zip docs/cliffsDeltaeg.html docs/pycco.css cliffsDeltaeg.py eg.py
git add docs/* docs/zips/*

 [ "opt.py" -nt "docs/opt.html" ] && pycco opt.py
zip -qu docs/zips/opt.zip docs/opt.html docs/pycco.css opt.py
git add docs/* docs/zips/*

 [ "bootstrap.py" -nt "docs/bootstrap.html" ] && pycco bootstrap.py
zip -qu docs/zips/bootstrap.zip docs/bootstrap.html docs/pycco.css bootstrap.py
git add docs/* docs/zips/*

 [ "sampleeg.py" -nt "docs/sampleeg.html" ] && pycco sampleeg.py
zip -qu docs/zips/sampleeg.zip docs/sampleeg.html docs/pycco.css sampleeg.py thing.py num.py GLOBALS.py opt.py numbers.py sample.py bootstrap.py sym.py eg.py
git add docs/* docs/zips/*

 [ "ranges.py" -nt "docs/ranges.html" ] && pycco ranges.py
zip -qu docs/zips/ranges.zip docs/ranges.html docs/pycco.css ranges.py
git add docs/* docs/zips/*

 [ "thing.py" -nt "docs/thing.html" ] && pycco thing.py
zip -qu docs/zips/thing.zip docs/thing.html docs/pycco.css thing.py num.py GLOBALS.py opt.py numbers.py sample.py bootstrap.py sym.py
git add docs/* docs/zips/*

 [ "rangeseg.py" -nt "docs/rangeseg.html" ] && pycco rangeseg.py
zip -qu docs/zips/rangeseg.zip docs/rangeseg.html docs/pycco.css rangeseg.py ranges.py eg.py
git add docs/* docs/zips/*

 [ "egeg.py" -nt "docs/egeg.html" ] && pycco egeg.py
zip -qu docs/zips/egeg.zip docs/egeg.html docs/pycco.css egeg.py eg.py
git add docs/* docs/zips/*

 [ "src.py" -nt "docs/src.html" ] && pycco src.py
zip -qu docs/zips/src.zip docs/src.html docs/pycco.css src.py GLOBALS.py opt.py
git add docs/* docs/zips/*

 [ "num.py" -nt "docs/num.html" ] && pycco num.py
zip -qu docs/zips/num.zip docs/num.html docs/pycco.css num.py GLOBALS.py opt.py
git add docs/* docs/zips/*

 [ "eg.py" -nt "docs/eg.html" ] && pycco eg.py
zip -qu docs/zips/eg.zip docs/eg.html docs/pycco.css eg.py
git add docs/* docs/zips/*

 [ "GLOBALS.py" -nt "docs/GLOBALS.html" ] && pycco GLOBALS.py
zip -qu docs/zips/GLOBALS.zip docs/GLOBALS.html docs/pycco.css GLOBALS.py opt.py
git add docs/* docs/zips/*

 [ "sandbox.py" -nt "docs/sandbox.html" ] && pycco sandbox.py
zip -qu docs/zips/sandbox.zip docs/sandbox.html docs/pycco.css sandbox.py
git add docs/* docs/zips/*

 [ "numeg.py" -nt "docs/numeg.html" ] && pycco numeg.py
zip -qu docs/zips/numeg.zip docs/numeg.html docs/pycco.css numeg.py thing.py num.py GLOBALS.py opt.py numbers.py sample.py bootstrap.py sym.py eg.py
git add docs/* docs/zips/*

 [ "numbers.py" -nt "docs/numbers.html" ] && pycco numbers.py
zip -qu docs/zips/numbers.zip docs/numbers.html docs/pycco.css numbers.py GLOBALS.py opt.py
git add docs/* docs/zips/*

 [ "sym.py" -nt "docs/sym.html" ] && pycco sym.py
zip -qu docs/zips/sym.zip docs/sym.html docs/pycco.css sym.py
git add docs/* docs/zips/*

 [ "sample.py" -nt "docs/sample.html" ] && pycco sample.py
zip -qu docs/zips/sample.zip docs/sample.html docs/pycco.css sample.py bootstrap.py num.py GLOBALS.py opt.py numbers.py
git add docs/* docs/zips/*

