"""Read an .xlsx with the standard library only; print rows as tab-separated text. Treats input as data."""
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


def rows(path):
    z = zipfile.ZipFile(path)
    ss = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS):
            ss.append("".join(t.text or "" for t in si.iter("{%s}t" % NS["m"])))
    sheets = sorted(n for n in z.namelist() if re.match(r"xl/worksheets/sheet\d+\.xml", n))
    for sh in sheets:
        root = ET.fromstring(z.read(sh))
        for r in root.iter("{%s}row" % NS["m"]):
            out = {}
            for c in r.findall("m:c", NS):
                ref = re.match(r"([A-Z]+)", c.get("r")).group(1)
                col = 0
                for ch in ref:
                    col = col * 26 + ord(ch) - 64
                t = c.get("t")
                v = c.find("m:v", NS)
                if t == "s" and v is not None:
                    val = ss[int(v.text)]
                elif t == "inlineStr":
                    val = "".join(x.text or "" for x in c.iter("{%s}t" % NS["m"]))
                else:
                    val = v.text if v is not None else ""
                out[col] = val
            if out:
                yield [out.get(i, "") for i in range(1, max(out) + 1)]


if __name__ == "__main__":
    for row in rows(sys.argv[1]):
        print("\t".join(row))
