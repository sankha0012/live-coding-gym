# Portuguese phrase bank

## The problem it solves

The interview may be in Portuguese. Technical words such as "pipeline", "trade-off" and "data leakage" stay in English in Brazilian tech teams, and the sentences around them are in Portuguese. This lesson gives the same six-step structure from the English lesson, with about 40 phrases you can say out loud. Practise them until they sound natural. This is optional, use it if you expect a Portuguese interview.

## The six steps in Portuguese

**1. O que faz**
- "Essa função recebe uma lista de eventos e devolve o último evento de cada usuário."
- "O objetivo é remover duplicados antes de calcular a métrica."
- "A entrada é um DataFrame e a saída é um dicionário."

**2. Como funciona**
- "A ideia principal é percorrer a lista uma vez e guardar o melhor valor num dicionário."
- "Primeiro eu valido a entrada, depois eu transformo, e no final eu devolvo o resultado."
- "Eu uso um set para checar a pertinência em tempo constante."
- "Eu ordeno por timestamp e pego o primeiro de cada grupo."

**3. Complexidade**
- "A complexidade de tempo é O(n), onde n é o número de linhas."
- "A ordenação domina, então fica O(n log n)."
- "O uso de memória é O(u), onde u é o número de usuários distintos."
- "Se não couber em memória, eu processo em chunks."

**4. Trade-offs**
- "Eu escolhi essa abordagem porque ela é simples e fácil de testar."
- "A alternativa seria ordenar tudo antes, mas isso custa mais memória."
- "Eu troco memória por velocidade."
- "É um trade-off entre legibilidade e performance."

**5. Riscos**
- "O principal risco é o input vazio ou com valores nulos."
- "Se dois eventos tiverem o mesmo timestamp, o resultado depende da ordem de entrada."
- "Se a API externa ficar lenta, o job pode travar, então eu uso timeout e retry com backoff."
- "Pode haver data leakage se o split não respeitar o tempo."
- "Se a mensagem chegar duas vezes, o consumidor precisa ser idempotente."

**6. Próximo passo**
- "Com mais tempo, eu adicionaria testes para os casos de borda."
- "Eu colocaria logs e uma métrica para monitorar a taxa de erro."
- "O próximo passo seria criar um alerta para drift."
- "Eu validaria isso com o time antes de colocar em produção."

## Pensando em voz alta

- "Deixa eu confirmar se entendi o problema."
- "Antes de codar, eu vou escrever os passos como comentários."
- "Vou testar com um exemplo pequeno primeiro."
- "Um caso de borda: e se a lista estiver vazia?"
- "Deixa eu pensar um segundo nessa parte."
- "Boa pergunta, eu não tenho certeza, mas eu verificaria assim."
- "Eu errei aqui, deixa eu corrigir."

## Sobre o uso de IA

- "Eu usei o assistente para o primeiro rascunho e depois revisei linha por linha."
- "Eu rodei o código num exemplo pequeno e adicionei testes para os casos de borda."
- "As decisões de design são minhas, o assistente só acelera a escrita."
- "Se eu não consigo explicar uma linha, eu simplifico antes de entregar."

## Sobre pontos fracos

- "Eu ainda estou ganhando velocidade para escrever código à mão, sem assistente."
- "Eu pratico todos os dias com exercícios cronometrados."
- "Enquanto isso, eu escrevo um teste primeiro e leio cada linha."

## The smallest runnable example

The point of the phrases is to describe code like this in Portuguese:

```python
def ultimo_por_usuario(eventos):
    melhor = {}
    for usuario, ts, valor in eventos:
        if usuario not in melhor or ts > melhor[usuario][0]:
            melhor[usuario] = (ts, valor)
    return {u: v for u, (ts, v) in melhor.items()}


print(ultimo_por_usuario([("a", 1, "x"), ("a", 3, "z")]))  # {'a': 'z'}
```

"Essa função devolve o último valor de cada usuário. Eu percorro a lista uma vez e guardo o par (timestamp, valor) mais recente num dicionário. É O(n) em tempo e O(u) em memória. O risco é o empate de timestamp. Com mais tempo, eu adicionaria um teste para esse caso."

## The three traps people hit

1. **Translating technical words.** Do not say "vazamento de dados de treino" for every case. Say "data leakage". Say "pipeline", "deploy", "drift", "timeout", "retry". Your listener expects them.
2. **Switching language in the middle of a sentence without control.** Keep the verbs and the sentence in Portuguese, and the technical noun in English. "Eu faço o merge das duas tabelas" is natural.
3. **Long sentences.** In a second language, short sentences are safer. One idea per sentence, as in the English structure.

## Say it like this

"Essa função recebe [entrada] e devolve [saída]. A ideia é [estrutura ou algoritmo]. A complexidade é [tempo] em tempo e [espaço] em memória, onde n é [o quê]. Eu escolhi [escolha] em vez de [alternativa] porque [motivo]. Os riscos são [dois riscos], e com mais tempo eu adicionaria [teste, log ou alerta]."

Record yourself saying this for three of your solved exercises. Listen once, fix the places where you stopped, and repeat the next day.
