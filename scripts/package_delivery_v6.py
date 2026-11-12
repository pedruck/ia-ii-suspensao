"""Create verified Overleaf and full-project ZIPs, excluding local/private state."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import zipfile

root = Path(__file__).resolve().parents[1]
output = Path.home()/'Downloads'
commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip()

def digest(data):
    return hashlib.sha256(data).hexdigest()

def archive(path, files, description):
    data = {name: p.read_bytes() for name, p in files.items()}
    manifest = {'description':description,'source_commit':commit,
                'files':{name:digest(content) for name,content in data.items()}}
    data['MANIFESTO_SHA256.json'] = json.dumps(manifest, indent=2, ensure_ascii=False).encode()
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
        for name, content in sorted(data.items()): z.writestr(name, content)
    with zipfile.ZipFile(path) as z:
        assert z.testzip() is None
        for name, expected in manifest['files'].items(): assert digest(z.read(name)) == expected
    return manifest

files = {name:root/'paper'/name for name in ['main.tex','main.pdf','results_v4.tex','IEEEtran.cls']}
files['LEIA-ME.md'] = root/'docs/ENTREGA_V6.md'
for p in (root/'figures/trajectory_v4').glob('*'):
    if p.suffix in ('.png','.pdf'):files['figures/'+p.name] = p
for name in ['ADEQUACAO_CRITERIOS_PROFESSOR.md','RESULTADOS_TRAJETORIAS_V4.md']:
    files['suplemento/'+name] = root/'docs'/name
for name in ['metrics.csv','verification.json','figure_selection.json','report_verification.json','tests.txt','local_checks.json']:
    files['suplemento/'+name] = root/'artifacts/trajectory_v4'/name
article = output/'artigo_suspensao_overleaf_v6.zip'
archive(article, files, 'Artigo IEEE com fonte Overleaf e suplemento; pesos e previsões no pacote completo.')
with tempfile.TemporaryDirectory() as directory:
    with zipfile.ZipFile(article) as z: z.extractall(directory)
    for _ in range(2):
        result = subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error','main.tex'],
                                cwd=directory, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        if result.returncode: raise RuntimeError(result.stdout[-5000:])
    info = subprocess.check_output(['pdfinfo','main.pdf'],cwd=directory,text=True)
    pages = int(next(line.split(':')[1] for line in info.splitlines() if line.startswith('Pages:')))
    assert pages <= 4, info
    log = (Path(directory)/'main.log').read_text()
    assert 'undefined references' not in log and 'Overfull' not in log
    shutil.copyfile(Path(directory)/'main.pdf', output/'artigo_suspensao_v6_trajetorias.pdf')

# Only committed repository files: no credentials, runs/, user assessments or raw data.
tracked = subprocess.check_output(['git','ls-files','-z'],cwd=root).decode().split('\0')
full_files = {n:root/n for n in tracked if n and (root/n).is_file()}
full = output/'projeto_suspensao_trajetorias_v6.zip'
archive(full, full_files, 'Projeto completo versionado, com modelos atuais e arquivos históricos identificados.')
print(json.dumps({'article':str(article),'project':str(full),'pdf':str(output/'artigo_suspensao_v6_trajetorias.pdf'),
                  'pages':pages,'source_commit':commit,'zip_checks_passed':True,'isolated_overleaf_build':True},indent=2))
