# Fork de tuya-vacuum + tuya-vacuum-maps Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Portar `jaidenlabelle/tuya-vacuum` (lib Python) e `jaidenlabelle/tuya-vacuum-maps` (integração HACS) para dois forks ativos em `porklabz/`, com o fix de CI do PR #7 aplicado na lib e o addon apontando para a lib forkada.

**Architecture:** Dois repositórios git independentes, cada um recebendo o histórico completo do respectivo upstream via `git merge --allow-unrelated-histories`. A lib (`tuya-vacuum-alternative`) ganha só o fix de CI + README de fork. O addon (`tuya-vacuum-maps`) tem seu domain do Home Assistant renomeado (`tuya_vacuum_maps` → `tuya_vacuum_maps_alternative`) e seu `manifest.json` passa a instalar a lib via git URL com tag fixa, em vez do pacote `tuya-vacuum` do PyPI.

**Tech Stack:** Python 3.13 (CI) / Python local para validação, Home Assistant custom integration (HACS), git.

**Spec:** [docs/superpowers/specs/2026-09-07-tuya-vacuum-hacs-fork-design.md](../specs/2026-09-07-tuya-vacuum-hacs-fork-design.md)

## Global Constraints

- Domain novo do addon: `tuya_vacuum_maps_alternative` (não colide com o original, não é drop-in automático).
- Tag da lib fork referenciada pelo addon: `v0.1.9-1` (versão upstream atual `0.1.9` + sufixo de patch do fork).
- URL de requirement no `manifest.json` do addon: `tuya-vacuum @ git+https://github.com/porklabz/tuya-vacuum-alternative.git@v0.1.9-1`.
- Sem publicação no PyPI. Sem CI/CD de release automatizado — fora de escopo.
- Mantém `LICENSE` MIT original (copyright Jaiden Labelle) em ambos os repos — sem modificação de copyright, só nota de fork no README.
- Nenhuma lógica de decodificação de mapa, `camera.py` ou `config_flow.py` muda além da troca do `DOMAIN` no addon.
- Handle GitHub do autor do fork: `fontenele` (usado em `codeowners` do manifest.json).

---

## Diretórios de trabalho

- Lib: `D:\www\porklabz\tuya-vacuum-alternative` (bash: `/d/www/porklabz/tuya-vacuum-alternative`) — remote `origin` já aponta para `git@github.com:porklabz/tuya-vacuum-alternative.git`, repo remoto vazio (só README inicial).
- Addon: `D:\www\porklabz\tuya-vacuum-maps` (bash: `/d/www/porklabz/tuya-vacuum-maps`) — remote `origin` já aponta para `git@github.com:porklabz/tuya-vacuum-maps.git`, repo remoto vazio (só README inicial).

Upstreams:
- Lib: `https://github.com/jaidenlabelle/tuya-vacuum.git` (branch `main`, tags até `v0.1.9`, versão atual em `pyproject.toml` é `0.1.9`).
- Addon: `https://github.com/jaidenlabelle/tuya-vacuum-maps.git` (branch `main`).

---

### Task 1: Trazer histórico e código upstream para tuya-vacuum-alternative (lib)

**Files:**
- Modify: `README.md` (resolução de conflito de merge, conteúdo temporário — reescrito na Task 3)
- Create: todo o restante da árvore do upstream (`pyproject.toml`, `requirements.txt`, `tuya_vacuum/`, `tests/`, `.github/workflows/test.yml`, `.vscode/`, `scripts/`, `LICENSE`)

**Interfaces:**
- Consumes: nada (primeira task)
- Produces: árvore de arquivos completa da lib upstream em `/d/www/porklabz/tuya-vacuum-alternative`, pronta para a Task 2 editar `.github/workflows/test.yml`

- [ ] **Step 1: Adicionar o remote upstream e buscar seu histórico**

```bash
cd /d/www/porklabz/tuya-vacuum-alternative
git remote add upstream https://github.com/jaidenlabelle/tuya-vacuum.git
git fetch upstream
```

Expected: fetch completa sem erro, mostrando `main` entre as branches buscadas.

- [ ] **Step 2: Fazer merge do histórico upstream (históricos não relacionados)**

```bash
git merge upstream/main --allow-unrelated-histories -m "Merge upstream jaidenlabelle/tuya-vacuum@main"
```

Expected: o merge para com conflito em `README.md` (ambos os lados criaram o arquivo com conteúdo diferente). A saída deve mostrar `CONFLICT (add/add): Merge conflict in README.md`.

- [ ] **Step 3: Resolver o conflito aceitando o README do upstream**

```bash
git checkout --theirs README.md
git add README.md
git commit --no-edit
```

Expected: `git commit` conclui o merge sem erro (mensagem "Merge upstream jaidenlabelle/tuya-vacuum@main").

- [ ] **Step 4: Verificar que a árvore de arquivos bate com o esperado**

```bash
find . -not -path './.git*' -type f | sort
```

Expected: lista inclui `LICENSE`, `README.md`, `pyproject.toml`, `requirements.txt`, `.github/workflows/test.yml`, `scripts/download_and_parse.py`, `tests/test_tuya.py`, `tests/test_vacuum.py`, `tests/test_vacuum_map_layout.py`, `tests/test_vacuum_map_path.py`, `tuya_vacuum/__init__.py`, `tuya_vacuum/const.py`, `tuya_vacuum/errors.py`, `tuya_vacuum/lz4.py`, `tuya_vacuum/map/__init__.py`, `tuya_vacuum/map/layout.py`, `tuya_vacuum/map/map.py`, `tuya_vacuum/map/path.py`, `tuya_vacuum/map/room.py`, `tuya_vacuum/tuya.py`, `tuya_vacuum/utils.py`.

Não há commit adicional neste step — o commit já foi feito no Step 3.

---

### Task 2: Aplicar o fix de CI do PR #7 na lib

**Files:**
- Modify: `.github/workflows/test.yml`

**Interfaces:**
- Consumes: árvore de arquivos produzida pela Task 1
- Produces: CI pinado em Python 3.13, pronto para a Task 3 reescrever README/pyproject e taguear

- [ ] **Step 1: Editar o pin de versão do Python no workflow**

Arquivo: `.github/workflows/test.yml`. Trocar:

```yaml
        with:
          # Semantic version range syntax or exact verison of a Python version
          python-version: "3.x"
```

por:

```yaml
        with:
          # Pinned so CI doesn't silently pick up a new Python release before
          # the pinned dependencies in requirements.txt ship wheels for it.
          python-version: "3.13"
```

- [ ] **Step 2: Validar que o YAML continua sintaticamente válido**

```bash
cd /d/www/porklabz/tuya-vacuum-alternative
python -c "import yaml; yaml.safe_load(open('.github/workflows/test.yml')); print('yaml ok')"
```

Expected: imprime `yaml ok` sem exceção.

- [ ] **Step 3: Conferir o diff antes de commitar**

```bash
git diff .github/workflows/test.yml
```

Expected: mostra exatamente a troca do comentário e da linha `python-version`, nenhuma outra linha alterada.

- [ ] **Step 4: Commit**

```bash
git add .github/workflows/test.yml
git commit -m "$(cat <<'EOF'
Fix CI: pin Python version to unbreak dependency install

Applies jaidenlabelle/tuya-vacuum#7 (upstream PR by fontenele, not
merged by the maintainer). "3.x" was resolving to Python 3.14, which
has no prebuilt wheels for pillow==11.0.0, breaking dependency
install in CI. Pinning to 3.13 keeps installs on prebuilt wheels.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

Expected: commit criado com sucesso.

---

### Task 3: Reescrever README, atualizar URLs do pyproject.toml, taguear e publicar a lib

**Files:**
- Modify: `README.md`, `pyproject.toml`

**Interfaces:**
- Consumes: estado da Task 2 (CI já corrigido)
- Produces: tag `v0.1.9-1` publicada em `origin` — a Task 6 depende dela existir no GitHub para referenciar no `manifest.json` do addon

- [ ] **Step 1: Reescrever o README com a nota de fork**

Substituir o conteúdo de `README.md` por:

```markdown
# tuya-vacuum (porklabz fork)

> **Este é um fork mantido de [jaidenlabelle/tuya-vacuum](https://github.com/jaidenlabelle/tuya-vacuum).**
> O mantenedor original não está fazendo merge de Pull Requests há vários meses.
> Este fork aplica [jaidenlabelle/tuya-vacuum#7](https://github.com/jaidenlabelle/tuya-vacuum/pull/7)
> (fix de CI) e outras correções pendentes, para manter a lib instalável e a
> integração [tuya-vacuum-maps](https://github.com/porklabz/tuya-vacuum-maps)
> funcionando.

tuya-vacuum is a python library to view maps from Tuya robot vacuums.

## Installation
Instale direto deste fork via pip + git:

```bash
pip install "tuya-vacuum @ git+https://github.com/porklabz/tuya-vacuum-alternative.git@v0.1.9-1"
```

## Usage
```python
from tuya_vacuum import TuyaVacuum

# Create a new TuyaVacuum instance
vacuum = TuyaVacuum(
    origin="https://openapi.tuyaus.com",
    client_id="<Client ID>",
    client_secret="<Client Secret>",
    device_id="<Device ID>"
)

# Parse the map data
vacuum_map = vacuum.fetch_realtime_map()

# Save the map as an image
image = vacuum_map.to_image()
image.save("output.png")
```

## Compatability List

This is a list of all currently tested devices. Create a new [issue](https://github.com/porklabz/tuya-vacuum-alternative/issues) to add your device.

| Device                                                | Support                           |
| ----------------------------------------------------- | --------------------------------- |
| [Lefant M1](https://www.lefant.com/en-ca/products/m1) | <text style="color:lightgreen">Supported</text> |
| Kabum Robô Aspirador de Pó 700                        | <text style="color:lightgreen">Supported</text> |

## Special Thanks
- [Jaiden Labelle](https://github.com/jaidenlabelle) for the original `tuya-vacuum` library
- [Tuya Cloud Vacuum Map Extractor](https://github.com/oven-lab/tuya_cloud_map_extractor) by [@oven-lab](https://github.com/oven-lab)
```

- [ ] **Step 2: Atualizar as URLs do projeto em pyproject.toml**

Em `pyproject.toml`, trocar:

```toml
[project.urls]
Homepage = "https://github.com/jaidenlabelle/tuya-vacuum"
Issues = "https://github.com/jaidenlabelle/tuya-vacuum/issues"
```

por:

```toml
[project.urls]
Homepage = "https://github.com/porklabz/tuya-vacuum-alternative"
Issues = "https://github.com/porklabz/tuya-vacuum-alternative/issues"
```

- [ ] **Step 3: Commit**

```bash
cd /d/www/porklabz/tuya-vacuum-alternative
git add README.md pyproject.toml
git commit -m "$(cat <<'EOF'
Reescreve README e URLs do projeto para o fork porklabz

Documenta o motivo do fork (upstream sem merges de PR), credita
jaidenlabelle pelo projeto original, e aponta Homepage/Issues do
pyproject.toml para o novo repositorio.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 4: Criar a tag v0.1.9-1**

```bash
git tag -a v0.1.9-1 -m "v0.1.9-1: upstream v0.1.9 + CI fix (jaidenlabelle/tuya-vacuum#7)"
```

- [ ] **Step 5: Push da branch e da tag**

```bash
git push origin main --follow-tags
```

Expected: push conclui sem erro; a saída lista tanto o update de `main` quanto a nova tag `v0.1.9-1`.

- [ ] **Step 6: Confirmar que a tag está visível no remoto**

```bash
git ls-remote --tags origin | grep v0.1.9-1
```

Expected: uma linha com o SHA da tag `refs/tags/v0.1.9-1`.

---

### Task 4: Trazer histórico e código upstream para tuya-vacuum-maps (addon)

**Files:**
- Modify: `README.md` (resolução de conflito de merge, conteúdo temporário — reescrito na Task 7)
- Create: todo o restante da árvore do upstream (`custom_components/tuya_vacuum_maps/`, `hacs.json`, `scripts/`, `tests/`, `.vscode/`, `LICENSE`)

**Interfaces:**
- Consumes: nada (independente das Tasks 1-3, mas o push final da Task 7 depende da tag da Task 3 existir)
- Produces: árvore de arquivos completa do addon upstream em `/d/www/porklabz/tuya-vacuum-maps`, pronta para a Task 5 renomear o domain

- [ ] **Step 1: Adicionar o remote upstream e buscar seu histórico**

```bash
cd /d/www/porklabz/tuya-vacuum-maps
git remote add upstream https://github.com/jaidenlabelle/tuya-vacuum-maps.git
git fetch upstream
```

Expected: fetch completa sem erro, mostrando `main` entre as branches buscadas.

- [ ] **Step 2: Fazer merge do histórico upstream (históricos não relacionados)**

```bash
git merge upstream/main --allow-unrelated-histories -m "Merge upstream jaidenlabelle/tuya-vacuum-maps@main"
```

Expected: o merge para com conflito em `README.md` (`CONFLICT (add/add): Merge conflict in README.md`).

- [ ] **Step 3: Resolver o conflito aceitando o README do upstream**

```bash
git checkout --theirs README.md
git add README.md
git commit --no-edit
```

Expected: `git commit` conclui o merge sem erro.

- [ ] **Step 4: Verificar que a árvore de arquivos bate com o esperado**

```bash
find . -not -path './.git*' -type f | sort
```

Expected: lista inclui `LICENSE`, `README.md`, `hacs.json`, `custom_components/tuya_vacuum_maps/__init__.py`, `custom_components/tuya_vacuum_maps/camera.py`, `custom_components/tuya_vacuum_maps/config_flow.py`, `custom_components/tuya_vacuum_maps/const.py`, `custom_components/tuya_vacuum_maps/manifest.json`, `scripts/download_maps.py`, `scripts/parse_map_data.py`, `tests/__init__.py`, `tests/layout.bin`.

Não há commit adicional neste step — o commit já foi feito no Step 3.

---

### Task 5: Renomear o domain do addon (tuya_vacuum_maps → tuya_vacuum_maps_alternative)

**Files:**
- Rename: `custom_components/tuya_vacuum_maps/` → `custom_components/tuya_vacuum_maps_alternative/`
- Modify: `custom_components/tuya_vacuum_maps_alternative/const.py`, `scripts/download_maps.py`, `scripts/parse_map_data.py`

**Interfaces:**
- Consumes: árvore produzida pela Task 4
- Produces: pasta e `DOMAIN` renomeados; a Task 6 edita `manifest.json` dentro dessa pasta já renomeada

- [ ] **Step 1: Renomear a pasta do componente**

```bash
cd /d/www/porklabz/tuya-vacuum-maps
git mv custom_components/tuya_vacuum_maps custom_components/tuya_vacuum_maps_alternative
```

Expected: `git status` mostra os arquivos como renamed (`R`).

- [ ] **Step 2: Atualizar o DOMAIN em const.py**

Em `custom_components/tuya_vacuum_maps_alternative/const.py`, trocar:

```python
DOMAIN = "tuya_vacuum_maps"
```

por:

```python
DOMAIN = "tuya_vacuum_maps_alternative"
```

- [ ] **Step 3: Atualizar o import em scripts/download_maps.py**

Em `scripts/download_maps.py`, trocar:

```python
from custom_components.tuya_vacuum_maps.tuya import TuyaCloudAPI
```

por:

```python
from custom_components.tuya_vacuum_maps_alternative.tuya import TuyaCloudAPI
```

- [ ] **Step 4: Atualizar o import em scripts/parse_map_data.py**

Em `scripts/parse_map_data.py`, trocar:

```python
from custom_components.tuya_vacuum_maps.vacuum_map import VacuumMap
```

por:

```python
from custom_components.tuya_vacuum_maps_alternative.vacuum_map import VacuumMap
```

- [ ] **Step 5: Confirmar que não sobrou nenhuma referência ao domain antigo**

```bash
grep -rn 'tuya_vacuum_maps"' custom_components/ 2>&1
grep -rn 'custom_components\.tuya_vacuum_maps\.' scripts/ 2>&1
```

Expected: ambos os comandos não retornam nenhuma linha (o primeiro busca `DOMAIN = "tuya_vacuum_maps"` exato entre aspas; o segundo busca imports do módulo antigo exato, sem pegar `tuya_vacuum_maps_alternative` por engano graças ao `.` logo após `maps`).

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -m "$(cat <<'EOF'
Renomeia domain para tuya_vacuum_maps_alternative

Usa um domain diferente do original para permitir instalar este fork
lado a lado com a integracao tuya_vacuum_maps original, sem forcar
migracao de quem ja usa o addon original.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 6: Apontar manifest.json e hacs.json para o fork

**Files:**
- Modify: `custom_components/tuya_vacuum_maps_alternative/manifest.json`, `hacs.json`

**Interfaces:**
- Consumes: pasta renomeada pela Task 5; tag `v0.1.9-1` publicada pela Task 3 (usada na URL de `requirements`)
- Produces: `manifest.json`/`hacs.json` prontos para a validação da Task 8

- [ ] **Step 1: Editar manifest.json**

Em `custom_components/tuya_vacuum_maps_alternative/manifest.json`, trocar o conteúdo completo por:

```json
{
    "domain": "tuya_vacuum_maps_alternative",
    "name": "Tuya Vacuum Maps Alternative",
    "codeowners": [
        "@fontenele"
    ],
    "config_flow": true,
    "dependencies": [],
    "documentation": "https://github.com/porklabz/tuya-vacuum-maps",
    "integration_type": "device",
    "iot_class": "cloud_polling",
    "issue_tracker": "https://github.com/porklabz/tuya-vacuum-maps/issues",
    "requirements": [
        "tuya-vacuum @ git+https://github.com/porklabz/tuya-vacuum-alternative.git@v0.1.9-1"
    ],
    "version": "0.1.4"
}
```

- [ ] **Step 2: Editar hacs.json**

Em `hacs.json`, trocar o conteúdo completo por:

```json
{
    "name": "Tuya Vacuum Maps Alternative",
    "country": ["CA", "US"]
}
```

- [ ] **Step 3: Validar que ambos os JSONs são sintaticamente válidos**

```bash
cd /d/www/porklabz/tuya-vacuum-maps
python -m json.tool custom_components/tuya_vacuum_maps_alternative/manifest.json > /dev/null && echo "manifest.json ok"
python -m json.tool hacs.json > /dev/null && echo "hacs.json ok"
```

Expected: imprime `manifest.json ok` e `hacs.json ok`, sem erro de parsing.

- [ ] **Step 4: Commit**

```bash
git add custom_components/tuya_vacuum_maps_alternative/manifest.json hacs.json
git commit -m "$(cat <<'EOF'
Aponta manifest.json e hacs.json para o fork

requirements agora instala a lib tuya-vacuum direto do fork
porklabz/tuya-vacuum-alternative via git URL fixada na tag v0.1.9-1,
em vez do pacote tuya-vacuum==0.1.8 do PyPI. documentation/issue_tracker
e codeowners atualizados para o fork; hacs.json com o novo nome.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 7: Reescrever README do addon e publicar

**Files:**
- Modify: `README.md`

**Interfaces:**
- Consumes: estado da Task 6
- Produces: branch `main` publicada em `origin` — usada pela validação manual da Task 8

- [ ] **Step 1: Reescrever o README com a nota de fork**

Substituir o conteúdo de `README.md` por:

```markdown
# Tuya Vacuum Maps Alternative

> **Este é um fork mantido de [jaidenlabelle/tuya-vacuum-maps](https://github.com/jaidenlabelle/tuya-vacuum-maps).**
> O mantenedor original não está fazendo merge de Pull Requests há vários
> meses. Este fork usa o domain `tuya_vacuum_maps_alternative` (diferente
> do original), então pode ser instalado lado a lado com a integração
> original sem conflito — mas quem migra do original precisa reconfigurar
> a integração do zero. A lib de decodificação de mapa também é um fork
> mantido: [porklabz/tuya-vacuum-alternative](https://github.com/porklabz/tuya-vacuum-alternative).

🏠 View Real-Time Vacuum Maps In Home Assistant.<br>
This component adds a new camera which polls the Tuya Cloud API for the latest realtime map data.<br>
This project is primarily focused on Lefant vacuums, but aims to support all Tuya vacuums.

## Disclaimer: Supporting More Vacuums
Adding support for new vacuums is very difficult. To quote the developer of the now-discontinued `tuya_cloud_map_extractor`:

> However, compatibility with other Tuya-based vacuums is limited and often inconsistent. Adding support for new models typically requires extensive reverse engineering, decoding binary map data, and handling manufacturer-specific quirks—for each individual device or firmware version.

Since I do not have access to any of these vacuums, and since they all have different protocols and map formats without any documentation, I need you to contribute to this project with the fix for your vacuum:

- You can look through the code to see how it decodes the map format, and then download a map file from your vacuum to see what causes the error. See the [instructions for setting up a developement environment](#development-environment).
- Fix the problem for your vacuum.
- Write unit tests, and include a copy of the map and path data files for your vacuum, so that I can verify any future updates do not undo your fix.
- Create a Pull Request to merge your fixes with this repository.


## Installation

### Installing Manually

To install this integration manually, add the contents of `custom_components` to your Home Assistants `custom_components` folder and reboot.

### Installing using HACS

1. [Install HACS](https://www.hacs.xyz/docs/use/) if its not already installed.
1. Add this repository (`porklabz/tuya-vacuum-maps`) to HACS by following this guide: [HACS: Add Custom Repository](https://www.hacs.xyz/docs/faq/custom_repositories/).
3. Search for "Tuya Vacuum Maps Alternative" using the HACS browser inside Home Assistant, and install.

## Compatibility List

This is a list of tested devices.
Create a new [issue](https://github.com/porklabz/tuya-vacuum-maps/issues) to add your device.

| Device                                                | Support                           |
| ----------------------------------------------------- | --------------------------------- |
| Lefant M1 | Supported |
| Lefant M2 Pro | Supported |
| Lefant N3 | Supported |
| Lebluelu SL60D | Supported |
| Lebluelu SL68 | Supported |
| Neatsvor X600 Pro | Supported |

## Development Environment

It's recommended to set up a development environment if you want to make changes to this component.

### Prerequisites

- [A Visual Studio Code + devcontainer development environment](https://developers.home-assistant.io/docs/development_environment)

### Getting Started

1. Once the devcontainer is created, fork this repository.
2. Go to the folder containing the `homeassistant-core` folder, it should be called `workspaces`.
3. Once your fork is created, make sure your terminal path is set to `/workspaces` and run `git clone <url>`.
4. To make testing easier, create a symlink to the component in your Home Assistant devcontainer.
   - Example: `ln -s /workspaces/tuya-vacuum-maps/custom_components/tuya_vacuum_maps_alternative /workspaces/homeassistant-core/config/custom_components`
5. For development, it's recommended you use a virtual environment.
   1. Create a new virtual environment (Run in the root `/tuya-vacuum-maps` folder):
      - `python -m venv venv`
   2. Activate the virtual environment:
      - `source ./venv/bin/activate`

## Special Thanks

- [Jaiden Labelle](https://github.com/jaidenlabelle) for the original `tuya-vacuum-maps` integration
- [Tuya Cloud Vacuum Map Extractor](https://github.com/oven-lab/tuya_cloud_map_extractor) by [@oven-lab](https://github.com/oven-lab)
```

- [ ] **Step 2: Commit**

```bash
cd /d/www/porklabz/tuya-vacuum-maps
git add README.md
git commit -m "$(cat <<'EOF'
Reescreve README para o fork porklabz

Documenta o motivo do fork, o novo domain (instalavel lado a lado com
o original), o link para a lib fork tuya-vacuum-alternative, e ajusta
instrucoes de instalacao/dev environment para o novo nome de pasta.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 3: Push**

```bash
git push origin main
```

Expected: push conclui sem erro.

---

### Task 8: Validação final

**Files:**
- Nenhum arquivo de produto é criado; task só roda comandos de verificação (pode usar um diretório temporário fora dos dois repos, ex. `/tmp` ou o scratchpad da sessão).

**Interfaces:**
- Consumes: estado publicado das Tasks 3 e 7 (tag da lib no GitHub, addon publicado no GitHub)
- Produces: confirmação de que a instalação via pip funciona e que a suíte de testes existente da lib passa — nada consumido por tasks futuras (última task do plano)

- [ ] **Step 1: Instalar a lib fork via pip em um venv isolado**

```bash
cd /tmp
rm -rf tuya-vacuum-smoke-test
python -m venv tuya-vacuum-smoke-test
source tuya-vacuum-smoke-test/Scripts/activate 2>/dev/null || source tuya-vacuum-smoke-test/bin/activate
pip install "tuya-vacuum @ git+https://github.com/porklabz/tuya-vacuum-alternative.git@v0.1.9-1"
```

Expected: pip resolve e instala a partir da tag `v0.1.9-1` sem erro (o `git+https` URL do `manifest.json` é exatamente essa string, então isso valida o requirement do addon).

- [ ] **Step 2: Confirmar que o pacote importa corretamente**

```bash
python -c "from tuya_vacuum import TuyaVacuum; print('import ok')"
deactivate
```

Expected: imprime `import ok`.

- [ ] **Step 3: Rodar a suíte de testes existente da lib no repo fork**

```bash
cd /d/www/porklabz/tuya-vacuum-alternative
python -m venv .venv-test
source .venv-test/Scripts/activate 2>/dev/null || source .venv-test/bin/activate
pip install -r requirements.txt
pip install pytest pytest-cov
pytest ./tests --doctest-modules
deactivate
rm -rf .venv-test
```

Expected: todos os testes existentes passam (mesma suíte do upstream, sem modificação — isso confirma que o fix de CI e o restante do port não quebrou nada). Se a instalação de dependências falhar por falta de wheel do `pillow` (mesmo problema do PR #7, mas agora rodando localmente numa versão de Python mais nova que 3.13), isso é esperado e não é um problema do fork — documente o resultado e prossiga; o CI do GitHub Actions já está pinado em 3.13 pela Task 2.

- [ ] **Step 4: Checar não há resíduo de referências ao domain antigo no addon**

```bash
cd /d/www/porklabz/tuya-vacuum-maps
grep -rn 'tuya_vacuum_maps"' custom_components/ && echo "FALHA: ainda ha domain antigo" || echo "ok: nenhum residuo"
```

Expected: imprime `ok: nenhum residuo`.

- [ ] **Step 5: Registrar o resultado da validação**

Sem commit nesta task — é validação read-only. Reporte ao usuário o resultado de cada step (pip install, import, pytest, grep) antes de considerar o plano concluído.
