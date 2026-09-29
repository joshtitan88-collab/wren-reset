# Rebuilds the site and the buyer ZIP from bundle/ (see .github/workflows/build.yml).
import base64, glob, hashlib, io, os, re, shutil, sys, tarfile, zipfile, zlib
from reportlab.pdfbase.pdfdoc import PDFBase85Encode as A85

DEST = "dl-30b9a3671e3d37e6/30-day-reset-v1.zip"
ORDER = ["30-day-reset-guide.pdf", "tracker.pdf", "tracker.html", "50-prompts.pdf",
         "30-day-reset-guide.md", "tracker.md", "50-prompts.md"]

data = base64.b64decode("".join(open(p).read() for p in sorted(glob.glob("bundle/part-*.b64"))))
want = open("bundle/SHA256").read().split()[0]
got = hashlib.sha256(data).hexdigest()
if got != want:
    sys.exit(f"bundle sha256 mismatch: {got} != {want}")
tmp = "/tmp/rebuild"
shutil.rmtree(tmp, ignore_errors=True)
tarfile.open(fileobj=io.BytesIO(data), mode="r:xz").extractall(tmp, filter="data")

shutil.copytree(os.path.join(tmp, "site"), ".", dirs_exist_ok=True)

src = os.path.join(tmp, "zipsrc")
pat = re.compile(rb"(>>\nstream\n)(.*?)(endstream)", re.S)
def enc(m):
    e = A85.encode(zlib.compress(m.group(2)))
    return m.group(1) + (e.encode("latin1") if isinstance(e, str) else e) + m.group(3)
for raw in glob.glob(os.path.join(src, "*.pdfraw")):
    with open(raw[:-3], "wb") as f:
        f.write(pat.sub(enc, open(raw, "rb").read()))

for line in open(os.path.join(src, "SHA256SUMS")):
    h, name = line.split()
    got = hashlib.sha256(open(os.path.join(src, name), "rb").read()).hexdigest()
    if got != h:
        sys.exit(f"{name}: sha256 mismatch {got} != {h}")
    print("ok", name)

os.makedirs(os.path.dirname(DEST), exist_ok=True)
with zipfile.ZipFile(DEST, "w", zipfile.ZIP_DEFLATED) as z:
    for name in ORDER:
        z.write(os.path.join(src, name), "30-day-reset/" + name)
print("wrote", DEST)
