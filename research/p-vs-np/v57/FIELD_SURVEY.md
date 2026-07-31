# Pesquisa bibliográfica da V57

## Range Avoidance

### GGNS — fronteira NC0_3

Karthik Gajulapalli, Alexander Golovnev, Satyajeet Nagargoje e Sidhant Saraogi, *Range Avoidance for Constant Depth Circuits: Hardness and Algorithms*, APPROX/RANDOM 2023, DOI 10.4230/LIPIcs.APPROX/RANDOM.2023.65.

O artigo registra que `NC0_2-Avoid` é polinomial e que `NC0_3-Avoid` permanece aberto no stretch mínimo. Também mostra que um algoritmo com oráculo NP no regime `m=n+n^(2/3)` implicaria matrizes rígidas explícitas e lower bounds superlineares para circuitos de profundidade logarítmica.

### Kuntewar–Sarma — subclasse monotônica

Neha Kuntewar e Jayalal Sarma, *Avoiding Range via Turan-Type Bounds*, APPROX/RANDOM 2025, DOI 10.4230/LIPIcs.APPROX/RANDOM.2025.62.

O trabalho resolve `Monotone-NC0_3-Avoid` para `m>n` por estruturas de Turán e loose cycles. Ele também trata portas de maioria em stretch maior, mas não fornece um algoritmo stretch-one geral para a órbita não monotônica `0x07`.

## Bijunctive CSP e 2-CNF

### Schaefer

Thomas J. Schaefer, *The Complexity of Satisfiability Problems*, STOC 1978, DOI 10.1145/800133.804350.

A classe bijuntiva pertence às famílias tratáveis da dicotomia de Schaefer e é representável por fórmulas 2-CNF.

### Redundância de fórmulas 2-CNF

Paolo Liberatore, *Redundancy in Logic II: 2CNF and Horn Propositional Formulae*, Artificial Intelligence 172(2–3), 2008, DOI 10.1016/j.artint.2007.06.003.

Esse trabalho estuda cláusulas redundantes, subconjuntos equivalentes irredundantes e mostra que a estrutura cíclica influencia a complexidade de diversas perguntas de minimização.

A V57 não reivindica novidade para a existência de fórmulas 2-CNF irredundantes. A diferença de escopo é que os blocos da V57 são fibras completas de portas locais, cada bloco contendo uma unidade e uma cláusula binária, e o objetivo é testar uma possível transferência do lema de blocos da V56 para Range Avoidance.

### Núcleos mínimos e testemunhas de insatisfatibilidade

- Vaibhav Karve e Anil N. Hirani, *The complete set of minimal simple graphs that support unsatisfiable 2-CNFs*, Discrete Applied Mathematics 283, 2020, DOI 10.1016/j.dam.2019.12.017.
- Joshua Buresh-Oppenheim e David Mitchell, *Minimum Witnesses for Unsatisfiable 2CNFs*, SAT 2006.

Esses trabalhos reforçam que estruturas mínimas e ciclos no grafo de implicação são objetos naturais. O gadget da V57 é satisfatível e irredundante, não um núcleo mínimo insatisfatível.

## Interpretação bibliográfica

A literatura torna improvável uma reivindicação de novidade ampla para “irredundância bijuntiva”. O possível conteúdo específico da V57 é mais estreito:

1. contraexemplo dentro de uma única órbita NPN ternária `0x07`;
2. stretch mínimo `m=n+1`;
3. orientação pela fibra pequena usada como tentativa natural de generalizar a V56;
4. família infinita obtida por soma direta;
5. conexão explícita com a fronteira de `NC0_3-Avoid`.

Essa prioridade ainda precisa ser confirmada por especialistas.
