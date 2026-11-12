"""Export the LSTM-only IEEE article and verify an isolated Overleaf build."""
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import zipfile

root=Path(__file__).resolve().parents[1]
output=Path.home()/'Downloads'
assert not subprocess.check_output(['git','status','--porcelain'],cwd=root,text=True), 'Commit changes before packaging'
commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
files={name:root/'paper'/name for name in ['main.tex','main.pdf','results_lstm_v5.tex','results_classes_v8.tex','IEEEtran.cls']}
files['LEIA-ME.md']=root/'docs/ENTREGA_V8.md'
for p in (root/'figures/lstm_study_v5').glob('*'):
    if p.suffix in ('.pdf','.png'):files['figures/'+p.name]=p
for name in ['ADEQUACAO_CRITERIOS_PROFESSOR.md','RESULTADOS_LSTM_V5.md']:
    files['suplemento/'+name]=root/'docs'/name
for name in ['metrics.csv','class_metrics.csv','provenance.json','figure_selection.json','class_verification.json','report_verification.json','indicators.json']:
    files['suplemento/'+name]=root/'artifacts/lstm_study_v5'/name
contents={name:p.read_bytes() for name,p in files.items()}
# The study's text, captions and numerical supplement must have the same scope.
for name,data in contents.items():
    if name.endswith(('.tex','.md','.csv','.json')):
        assert not re.search(r'\b(?:ARX|ridge|persist[eê]ncia|regress[aã]o)\b',data.decode(),re.I), name
manifest={'description':'Artigo IEEE: aplicação exclusiva da LSTM, tema II','source_commit':commit,
          'files':{name:hashlib.sha256(data).hexdigest() for name,data in contents.items()}}
contents['MANIFESTO_SHA256.json']=json.dumps(manifest,indent=2,ensure_ascii=False).encode()
archive=output/'artigo_suspensao_overleaf_v8_lstm_classes.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for name,data in sorted(contents.items()):z.writestr(name,data)
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    for name,digest in manifest['files'].items():assert hashlib.sha256(z.read(name)).hexdigest()==digest
with tempfile.TemporaryDirectory() as directory:
    with zipfile.ZipFile(archive) as z:z.extractall(directory)
    for _ in range(2):
        result=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error','main.tex'],cwd=directory,
                              stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,errors='replace')
        if result.returncode:raise RuntimeError(result.stdout[-5000:])
    info=subprocess.check_output(['pdfinfo','main.pdf'],cwd=directory,text=True)
    pages=int(next(line.split(':')[1] for line in info.splitlines() if line.startswith('Pages:')))
    assert pages<=4
    log=(Path(directory)/'main.log').read_text(errors='replace')
    assert 'undefined references' not in log and 'Overfull' not in log
    text=subprocess.check_output(['pdftotext','main.pdf','-'],cwd=directory,text=True)
    assert not re.search(r'\b(?:ARX|ridge|persist[eê]ncia|regress[aã]o)\b',text,re.I)
    pdf=output/'artigo_suspensao_v8_lstm_classes.pdf'
    shutil.copyfile(Path(directory)/'main.pdf',pdf)
report={'article':str(archive),'pdf':str(pdf),'pages':pages,'source_commit':commit,
        'zip_checks_passed':True,'isolated_overleaf_build':True,'lstm_only_text_check':True,
        'zip_sha256':hashlib.sha256(archive.read_bytes()).hexdigest()}
(output/'verificacao_entrega_suspensao_v8.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
