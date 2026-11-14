# pt-br-colab — avaliação e dúvidas sobre o Live Coding Gym

Autor: Pedro Gentil · Data: 2026-11-14 · Base avaliada: `main` @ `db40070`

Esta pasta guarda os comentários de colaboração em português. Nada aqui altera o código do app.
A seção final ("Questions for Sankhadip") está em inglês para ser encaminhada diretamente.

---

## 1. Sumário executivo

**O que é.** Um app local de treino (FastAPI + página HTML/JS sem build + SQLite) para levar uma pessoa
de "sei a teoria de Python e SQL, mas sempre programei com IA" até "pronta para uma entrevista de
live coding sobre engenharia de software para sistemas de ML em produção". A entrevista-alvo é a do
**iFood, na plataforma Coderbyte**. Escopo declarado: um único usuário, num Mac.

**Estado atual.** Construído em um único dia (22 commits em 14/11/2026), em par com o Claude, seguindo
spec → plano → TDD. O app já é usável de ponta a ponta. A spec ainda está marcada como
*"awaiting approval"*.

**Números.**

| Item | Valor |
|---|---|
| Etapas da jornada | 12 (Python à mão → rotina de live coding → SQL → código robusto → testes → dados reais → ferramentas de ML → ML em produção → falhas de modelo → uso de IA observado → explicar código → mocks) |
| Exercícios | ~258 (40 · 20 · 46 · 20 · 13 · 30 · 18 · 20 · 15 · 20 · 16; a etapa 12 sorteia dos marcados `mock: true`) |
| Tipos de exercício | python, sql, tests (escrever testes que pegam implementações com bug), quiz, open, prompt, explain |
| Código do app | ~10 módulos em `gym/` (~1.000 linhas) + 17 arquivos de teste |
| Avaliação | testes ocultos (pytest / SQLite em memória) + revisão por rubrica via Gemini |

**Pontos fortes.**

- Ideia pedagógica muito boa: ataca o gap real (recall e digitação, não compreensão) com 4 modos
  progressivos (redigitar → preencher lacunas → editor em branco → editor cronometrado), flashcards
  com caixas de Leitner e *gates* por etapa.
- Avalia o que a entrevista realmente avalia: além do código, o **prompt** usado com a IA e a
  **explicação** do candidato, inclusive com perguntas de follow-up no mock.
- Conteúdo de alta qualidade e bem focado em produção (ex.: alerta de drift com histerese, PSI,
  canary split, shadow compare, TTL cache, circuit breakers). Os testes ocultos que olhei cobrem bem
  bordas e casos de erro.
- Arquitetura enxuta e legível: stdlib onde possível (Gemini via `urllib`, `sqlite3`), conteúdo
  separado do código em arquivos planos, `check_content` garante que toda solução de referência passa
  nos próprios testes.
- Falhas do Gemini não perdem submissão (revisão fica *pending* e pode ser refeita).

**Pontos de atenção (resumo).** Higiene do repositório (cache do graphify versionado), ausência de
licença, divergência entre spec e código nos *gates*, score do mock penalizado quando o Gemini falha,
e um fluxo de trabalho (CLAUDE.md) que depende de ferramentas específicas — o que pesa quando houver
mais de um colaborador. Detalhes na seção 2.

**Veredito.** Projeto bem pensado, enxuto e já útil para o objetivo pessoal. Para virar uma colaboração
de fato, faltam decisões de escopo (ferramenta pessoal vs. produto para outras pessoas), de fluxo de
contribuição e de propriedade/licença.

---

## 2. Observações técnicas

> Nota: o repositório é privado e eu li o código pelo GitHub; **não rodei** `uv run pytest` nem o app.
> As observações abaixo são de leitura.

1. **Cache do graphify versionado.** `graphify-out/` tem ~1.700 arquivos de cache AST e um
   `graph.html` de ~3,5 MB — quase metade dos ~3.800 arquivos do repo. Com mais de um colaborador, a
   regra "inclua `graphify-out/` em todo commit" vai gerar conflitos de merge constantes em
   `graph.json`. Sugestão: colocar `graphify-out/cache/` (e talvez `graph.html`) no `.gitignore`.
2. **Sem LICENSE.** Vale definir antes de outras pessoas contribuírem.
3. **Spec x código nos gates.** A spec (seção 4, *Gates*) diz que **todo** drill obrigatório precisa
   passar e que **todo** critério da rubrica deve atingir o limiar. O último commit relaxou para 70%
   de aprovação e nota mínima 3 (`gates.py` usa `pass_ratio`). A spec não foi atualizada.
4. **Confiança no cliente.** `GET /api/exercise?mode=retype` devolve a solução; o `mode` e o
   `duration_s` do `POST /api/submit` vêm do navegador. Então dá para "passar em branco" depois de ver
   a solução, e o tempo do modo cronometrado não é medido no servidor. Para uso individual é aceitável
   (autodisciplina); para ranking ou multiusuário, precisaria de controle no servidor.
5. **Sem sandbox.** `runner.py` executa o código com o mesmo interpretador do servidor. Declarado fora
   de escopo e correto para uso pessoal — mas impede hospedar o app para outras pessoas.
6. **Score do mock quando o Gemini falha.** Revisões *pending* voltam com `scores = {}`; em
   `mock.score` isso vira `review_avg = 0`, o que derruba silenciosamente 40% do total e entra na média
   de prontidão. Sugestão: não fechar o mock (ou excluí-lo da prontidão) enquanto houver revisão
   pendente, e permitir *retry* das revisões do mock.
7. **Peso do SQL no mock.** O SQL conta como 1 teste ("result matches reference") contra N testes do
   Python no `pass_rate`, então o SQL quase não pesa no score.
8. **Erro na query de referência.** Em `check_sql`, a execução da solução de referência não está dentro
   do `try`; um erro de conteúdo vira 500. Baixo risco, porque `check_content` já protege.
9. **Dependência de rede e plataforma.** CodeMirror via CDN e Gemini exigem internet; README e CLAUDE.md
   assumem Mac + `uv` + Python 3.12. Rodar em Linux/Windows provavelmente funciona, mas não foi testado.
10. **Barreira de onboarding.** O CLAUDE.md torna obrigatórios plugins/skills específicos (Ponytail,
    Superpowers, Graphify, Caveman). Faz sentido para o autor, mas é preciso decidir se colaboradores
    também precisam usá-los.
11. **Modelo do Gemini fixo como padrão** (`gemini-3.1-flash-lite`) e provedor único. Uma pequena
    abstração permitiria usar outros provedores (Claude, OpenAI) por configuração, se for desejado.
12. **Conteúdo só em inglês.** Natural, mas como o iFood é uma empresa brasileira, pode valer ter
    termos e cenários do contexto brasileiro (e, se a entrevista puder ser em português, material em
    pt-BR).

---

## 3. Onde eu (Pedro) poderia contribuir

- Revisão de conteúdo das etapas 6–9 (dados reais, ML em produção, falhas de modelo).
- Contexto do mercado brasileiro / iFood e eventual versão pt-BR de lições e prompts.
- Fazer o papel de entrevistador humano em mocks.
- Melhorias pontuais: `.gitignore` do graphify, score do mock com revisões pendentes, provedor de LLM
  configurável, suporte multiplataforma.

---

## 4. Questions for Sankhadip (English, ready to forward)

**Goal and scope**

1. Is this purely your own prep for the iFood interview, or do you want it to become a tool other
   people can use? Do you already have an interview date?
2. What role would you like me to play: content author/reviewer, code reviewer, human mock
   interviewer, Brazil/iFood context, Portuguese localization — or something else?
3. Will the interview be in English or Portuguese? Would Portuguese content or Brazilian terminology
   help?
4. Do you have any concrete information about the iFood round (problem style, ML stack, how they
   score the AI prompt)? Has the content been checked against a real Coderbyte session?

**Design decisions**

5. The spec says every required drill must pass and every rubric criterion must meet the threshold;
   the last commit relaxed this to 70% and a minimum score of 3. Is the relaxed version the final
   rule? Should the spec be updated (it is still marked "awaiting approval")?
6. When Gemini is down, mock reviews stay pending with no scores, which counts as 0 for 40% of the mock
   total and lowers readiness. Is that intended, or should a mock wait for its reviews?
7. SQL counts as a single test in the mock pass rate, versus several Python tests. Should SQL carry a
   fixed weight instead?
8. Retype mode exposes the solution and the client sends `mode` and `duration_s`. Fine for a single
   user — do you ever plan multiple users, hosting, or a sandbox for running code?
9. Gemini only, or would you accept a small provider switch (Claude/OpenAI) via `.env`?

**Collaboration workflow**

10. How should I contribute: feature branches + pull requests, issues, or comments in this folder?
11. Should collaborators also follow the CLAUDE.md toolchain (Superpowers, Ponytail, Graphify,
    Caveman)?
12. `graphify-out/` (about 1,700 cache files and a 3.5 MB HTML graph) is committed and must be updated
    in every commit. With two people that will cause merge conflicts. OK to gitignore the cache and
    regenerate it locally?
13. Which license do you have in mind, and how would you like authorship credited?
14. Should it run on Linux/Windows too, or stay Mac-only?
