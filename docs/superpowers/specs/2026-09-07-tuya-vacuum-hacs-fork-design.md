# Fork mantido de tuya-vacuum + tuya-vacuum-maps

**Data:** 2026-09-07
**Status:** Aprovado para implementação

## Contexto e motivação

`jaidenlabelle/tuya-vacuum-maps` é uma integração custom (HACS) para Home
Assistant que exibe mapas em tempo real de aspiradores robôs Tuya via API
Tuya Cloud. Ela depende, via pip, da lib Python `jaidenlabelle/tuya-vacuum`
(publicada no PyPI), que decodifica os dados brutos do mapa.

O mantenedor original não faz merge de PRs há meses. guilherme@fontenele.net
tem um PR aberto (#7) em `tuya-vacuum` corrigindo o CI (pin de
`python-version` em `.github/workflows/test.yml`, que estava resolvendo para
Python 3.14 e quebrando a instalação de `pillow==11.0.0` por falta de
wheels pré-compiladas). Sem esse fix, o CI do fork ficaria vermelho.

Objetivo: manter dois forks ativos, publicáveis via HACS, que a comunidade
possa instalar como alternativa enquanto o repositório original ficar sem
manutenção.

## Arquitetura

Dois repositórios, espelhando a estrutura do upstream (facilita comparar e
puxar mudanças futuras do autor original):

```
porklabz/tuya-vacuum-alternative     fork de jaidenlabelle/tuya-vacuum (lib)
porklabz/tuya-vacuum-maps            fork de jaidenlabelle/tuya-vacuum-maps (addon HACS)
```

Ambos os repositórios remotos já existem no GitHub (confirmado via
`git ls-remote`) e estão vazios (só README inicial). Ambos os diretórios de
trabalho locais já existem:

- `D:\www\porklabz\tuya-vacuum-alternative` (repo da lib)
- `D:\www\porklabz\tuya-vacuum-maps` (repo do addon)

### 1. `porklabz/tuya-vacuum-alternative` — fork da lib

- Clone completo do histórico/código de `jaidenlabelle/tuya-vacuum`.
- Aplica o PR #7: em `.github/workflows/test.yml`, troca
  `python-version: "3.x"` por `python-version: "3.13"`, com o comentário
  do PR original ("Pinned so CI doesn't silently pick up a new Python
  release before the pinned dependencies in requirements.txt ship wheels
  for it.").
- Mantém `LICENSE` (MIT) com a atribuição original a jaidenlabelle — fork
  sob a mesma licença.
- README reescrito: explica que é um fork ativo mantido por falta de
  merges no upstream, linka o repositório original e o PR #7
  (`jaidenlabelle/tuya-vacuum#7`), e mantém as instruções de uso/instalação
  da lib (`pip install`) ajustadas para o novo pacote/origem.
- Após o primeiro commit, cria a tag `v0.1.8-1` (versão upstream + sufixo
  de patch do fork) — é essa tag que o addon vai referenciar.

### 2. `porklabz/tuya-vacuum-maps` — fork do addon HACS

- Clone completo do histórico/código de `jaidenlabelle/tuya-vacuum-maps`.
- Domain trocado em todo o `custom_components/`: `tuya_vacuum_maps` →
  `tuya_vacuum_maps_alternative`. Isso inclui:
  - nome da pasta `custom_components/tuya_vacuum_maps/` →
    `custom_components/tuya_vacuum_maps_alternative/`
  - `manifest.json` (`domain`)
  - toda referência interna ao domain em `.py` (const.py, `__init__.py`,
    config_flow, etc.) e em `strings.json`/`translations/*.json` se
    existirem
  - Domain novo e diferente do original é proposital: permite instalar o
    fork lado a lado com a integração original, sem migração forçada de
    quem já usa o addon original.
- `manifest.json`: `requirements` passa a ser
  `["tuya-vacuum @ git+https://github.com/porklabz/tuya-vacuum-alternative.git@v0.1.8-1"]`.
- `hacs.json`: atualiza `name` para refletir o fork (ex: "Tuya Vacuum Maps
  Alternative"); mantém `country`.
- README reescrito: explica o motivo do fork, créditos ao projeto
  original, instruções de instalação via HACS custom repository
  apontando para `porklabz/tuya-vacuum-maps`, e nota sobre o domain
  diferente (drop-in não automático — quem migra do original precisa
  reconfigurar a integração).
- Mantém `LICENSE` MIT original.

## O que NÃO muda

- Nenhuma lógica de decodificação de mapa, nenhuma lógica de
  `camera.py`/`config_flow` além da troca de domain. O comportamento
  funcional do addon é idêntico ao upstream.
- Sem publicação no PyPI — a lib é consumida direto via git URL no
  `manifest.json`, evitando overhead de conta/token PyPI.

## Testes

- CI de `tuya-vacuum-alternative`: já validado pelo próprio PR #7 (pin do
  Python 3.13); reaproveita a suíte de testes existente do upstream sem
  modificação.
- `tuya-vacuum-maps`: reaproveita a suíte/workflows existentes do
  upstream. Verificação manual pós-port: instalar a integração fork num
  Home Assistant local (ou devcontainer, como o projeto já recomenda) e
  confirmar que o `manifest.json` resolve a dependência git corretamente
  (`pip install` da URL com tag).

## Passos de rollout

1. Portar `tuya-vacuum-alternative` (lib): clone, aplica fix do CI,
   ajusta README/LICENSE, commit, tag `v0.1.8-1`, push.
2. Portar `tuya-vacuum-maps` (addon): clone, renomeia domain em todos os
   arquivos, ajusta `manifest.json`/`hacs.json`/README, commit, push.
   Depende do passo 1 estar publicado (tag precisa existir no GitHub
   antes do `manifest.json` do addon referenciá-la).
3. Validação manual: confirmar que `pip install` da URL git funciona
   (smoke test local) e que HACS reconhece `tuya-vacuum-maps` como
   repositório custom válido (hacs.json válido, estrutura de pastas
   correta).

## Fora de escopo

- Publicação no PyPI da lib fork.
- CI/CD de release automatizado (tags/releases futuras continuam manuais
  por enquanto).
- Suporte a novos modelos de aspirador além dos já suportados pelo
  upstream.
