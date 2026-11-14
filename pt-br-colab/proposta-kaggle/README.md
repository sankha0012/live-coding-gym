# Proposta: conteúdo inspirado no curso de Python da Kaggle

Autor: Pedro Gentil · 2026-11-14 · Base: `main` @ `db40070`

*English summary at the end.*

## Por que esta proposta

O curso [Learn Python da Kaggle](https://www.kaggle.com/learn/python) tem 7 aulas introdutórias, e a etapa 1 do gym
já cobre e ultrapassa esse conteúdo. O que vale trazer de lá não são os exercícios, mas três ideias:

1. **Explorar objetos sem autocomplete** (aula 7: `type()`, `dir()`, `help()`). A entrevista permite consultar
   documentação e o editor do gym não tem autocomplete, mas hoje o gym não treina essa habilidade.
2. **Sobrecarga de operadores em bibliotecas** (aula 7). Em pandas e NumPy isso vira bugs silenciosos: `and` em vez
   de `&`, precedência sem parênteses, `NaN != NaN`, `== None`, dtype que vira float e atribuição encadeada.
3. **Formatos de exercício diferentes**: "achar o bug", "prever a saída" e exercício **corrigido por métrica em dados
   novos**, como o blackjack da Kaggle, que é avaliado por simulação.

Todo o texto, código e testes abaixo são originais. Da Kaggle vieram só as ideias.

## O que tem aqui

A pasta `content/` espelha a estrutura do gym. Para adotar, basta copiar as pastas para `content/` e acrescentar os
cards ao `cards.yaml` da etapa.

| Etapa | Arquivo / exercício | Tipo | O que treina |
|---|---|---|---|
| 01 | `lessons/26-exploring-without-autocomplete.md` | lição | `type`, `dir`, `help`, `inspect.signature`, `vars`, rotina para objeto desconhecido |
| 01 | `cards-additions.yaml` | 6 cards | Para acrescentar ao `content/01-hand-python/cards.yaml` |
| 01 | `py1-fix-the-bugs` | python | Achar e corrigir 3 bugs: `return` dentro do loop, `if` em vez de `elif` com `None`, default mutável |
| 01 | `py1-predict-output` | quiz (12) | Aliasing, default mutável, `//`, `round`, float, short-circuit, imutabilidade, slicing, ordenação, grid `* n`, truthiness |
| 06 | `lessons/31-operator-traps-in-pandas.md` | lição | `&`/`\|`/`~`, parênteses, NaN, dtypes, agregações que pulam NaN, copy-on-write do pandas 3 |
| 06 | `pdx-boolean-mask` | python | Filtro com máscara booleana + comparação NaN-safe entre modelo atual e modelo shadow |
| 06 | `pdx-nan-quiz` | quiz (10) | As armadilhas da lição |
| 06 | `st-decision-stump` | python | **Corrigido por métrica**: stump treinado numa amostra e avaliado por acurácia (≥ 0,85) em outra semente; trata valores ausentes com fallback |

Decisões:

- Todos os exercícios estão com `required: false`, para não mexer nos gates sem você decidir.
- `pdx-boolean-mask` e `st-decision-stump` trazem soluções erradas em `wrong/`; o `check_content` confirma que os
  testes as reprovam.
- O formato "corrigido por métrica" não precisou de um tipo novo. Coube no `kind: python`: o teste oculto gera os
  dados com semente fixa e verifica um limiar de acurácia.

## Validação

Reproduzi localmente `gym/content.py`, `gym/runner.py` e as regras do `gym/check_content.py`, e rodei sobre esta
pasta com Python 3 e pandas 3.0.5:

- as 3 soluções de referência passam nos próprios testes (6, 7 e 8 testes);
- os starters não passam;
- as soluções em `wrong/` são reprovadas;
- os 2 quizzes carregam, com 22 perguntas no total, e as respostas foram conferidas executando cada trecho.

Ainda assim, vale rodar `uv run python -m gym.check_content` e `uv run pytest` depois de copiar para `content/`.

Observação: o `pyproject.toml` não fixa a versão do pandas. No pandas 3, o copy-on-write mudou o comportamento de
atribuição encadeada (não há mais `SettingWithCopyWarning`). A lição e o quiz já seguem o pandas 3. Talvez valha
fixar `pandas>=3` no projeto.

## Próximos passos possíveis

Os cursos seguintes da Kaggle combinam com outras etapas e podem render propostas parecidas:

- Advanced SQL → etapa 3;
- Data Cleaning → etapa 6;
- Intermediate ML (pipelines, validação cruzada) → etapa 7;
- Feature Engineering (target encoding sem vazamento) → etapa 8;
- ML Explainability (permutation importance, SHAP) → etapa 11.

---

## English summary

Ideas taken from Kaggle Learn's Python course (all text, code and tests are original):

- **Step 01:** a lesson on exploring objects without autocomplete (`type`, `dir`, `help`, `inspect.signature`), 6
  cards, a "fix the three bugs" exercise and a 12-question "predict the output" quiz.
- **Step 06:** a lesson on pandas/NumPy operator traps (including pandas 3 copy-on-write), a boolean-mask +
  NaN-safe shadow-comparison exercise, a 10-question quiz, and a **metric-graded** decision-stump exercise (trained
  on one seed, must reach ≥ 0.85 accuracy on another).

Every exercise is `required: false`. To adopt, copy the folders into `content/` and append the cards. I validated
them with a local copy of the loader, runner and `check_content` rules: reference solutions pass, starters fail, and
`wrong/` solutions are caught. Please still run `gym.check_content` and `pytest`. You may also want to pin
`pandas>=3`.
