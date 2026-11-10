# E se o Sol sumisse? — versão 1 (portão 1: pergunta e roteiro)

**Pergunta-mãe:** E se o Sol sumisse agora?

**A resposta que qualquer pessoa repete:** por oito minutos, nada muda, porque a luz e a gravidade do Sol ainda estão a caminho. Depois, o céu apaga, a Terra sai em linha reta e congela por cima, mas lá no fundo o mar continua líquido.

**Pergunta final (pessoal, de escolha, ligada ao tema):** E você, se soubesse, o que ia fazer nesses oito minutos?
Os "oito minutos" são plantados na segunda frase e pagos na pergunta final.

## Três curiosidades reais (com fonte no `roteiro.json`)

1. **Os oito minutos.** A luz do Sol leva em média 8 min 20 s para chegar aqui. A luz que já estava no caminho continua chegando, então ninguém perceberia nada nesse tempo.
2. **A gravidade também se atrasa.** Ela viaja na velocidade da luz (medido em 2017, quando as ondas gravitacionais e a luz de uma fusão de estrelas de nêutrons chegaram com 1,7 s de diferença depois de 130 milhões de anos de viagem). Por isso a Terra continua girando em volta do lugar vazio por oito minutos, e não sai voando na hora, como nos filmes.
3. **O gelo vira cobertor.** Em uma semana, a média da superfície cai para uns −18 °C; em um ano, para uns −73 °C (estimativa de David Stevenson, do Caltech). O mar congela por cima, mas o gelo isola a água de baixo, que continua líquida por muito tempo.

## Corrente de perguntas e ganchos (um a cada 10 a 12 s)

| Tempo (aprox.) | Gancho / pergunta aberta | Onde fecha |
|---|---|---|
| 0 s | E se o Sol sumisse agora? (o Sol some no meio da frase) | fim do vídeo |
| ~8 s | "Nos filmes, a Terra sairia voando na hora." (mostrado e desfeito com ◀◀) | "Mas a gravidade também viaja na velocidade da luz" |
| ~18 s | "a última luz chega, e o céu fica preto" → e a Terra? | "sai em linha reta" |
| ~28 s | o frio: uma semana, um ano | "o mar congela por cima" |
| ~38 s | "Mas o gelo vira um cobertor" (a virada) | "lá no fundo a água continua líquida" |
| ~45 s | Pergunta final dos oito minutos (fica no ar) | — |

## Um palco só (ideia → dispositivo)

O palco é o Sol embaixo e a Terra em cima (com a Lua), na vertical do 9:16 (`roll: 90`), como no `lua_mares`. Cada ideia entra **em cima do que já está na tela**: nada de cortar para outro lugar.

| Fala | Ideia | O que entra na tela (dispositivo) | Erro que evita |
|---|---|---|---|
| A1 | E se o Sol sumisse agora? | Sol embaixo, Terra e Lua em cima; o Sol some com um clarão no "sumisse" | — |
| A2–A3 | por oito minutos nada muda: a luz já está no caminho | um ponto de luz (a última luz) sai do lugar vazio e viaja devagar até a Terra; a Terra segue iluminada enquanto ele viaja | achar que a Terra apaga na hora |
| B1 | a versão de filme | a Terra dispara para fora da órbita no mesmo instante | — |
| B2 | a gravidade viaja na velocidade da luz | ◀◀ rebobina; uma onda transparente sai do lugar vazio junto com o ponto de luz, as duas no mesmo passo | achar que a gravidade é instantânea |
| B3 | a Terra continua girando em volta do nada | a órbita tracejada aparece; a Terra segue a curva em volta de um brilho fraco no lugar vazio | — |
| C1 | a última luz chega, o céu fica preto | o ponto de luz e a onda chegam juntos; o lado de dia da Terra apaga | — |
| C2 | até a Lua apaga | a Lua, iluminada até ali, apaga (ela só reflete o Sol) | achar que a Lua tem luz própria |
| C3 | a Terra sai em linha reta a 30 km/s | uma seta reta, tangente à órbita, sai da Terra e a Terra anda por ela, deixando a órbita para trás | achar que a Terra "cai", espirala ou sai em curva |
| D1–D2 | uma semana −18 °C; um ano −73 °C; o mar congela por cima | uma casca branca de gelo cobre a Terra e fica mais grossa | — |
| D3 | o gelo vira cobertor; lá no fundo a água continua líquida | a Terra se abre (corte): por baixo do gelo, o calor de dentro aceso | achar que o planeta vira gelo maciço na hora |
| Q1 | e você, nesses oito minutos? | a Terra no escuro, a órbita vazia; a câmera continua andando (sem fade) | — |

## Honestidade (o que o vídeo simplifica de propósito)

- **O Sol não pode sumir de verdade** (a massa e a energia não desaparecem). É um experimento de pensamento. Isso fica aqui, e não na fala: uma frase de calma no fim faria o vídeo parecer que acabou.
- **Fora de escala:** o Sol fica perto e pequeno no diagrama. O ponto de luz e a onda levam alguns segundos de vídeo, que representam os oito minutos.
- **"Oito minutos"** é o arredondamento de 8 min 20 s (varia de 8 min 10 s a 8 min 27 s ao longo do ano).
- **As temperaturas são da média da superfície** e são estimativas (outras fontes dão números diferentes para o fim do primeiro ano). A fala diz "a média".
- **A Lua continua presa à Terra** e vai junto na linha reta. A fala não entra nisso.

## Próximo portão

Com o sim do roteiro: voz-guia, plano de cenas (`plano.json`), quadros e rascunho com conferência. A voz final (ElevenLabs) e o render inteiro só no fim, cada um com o seu sim.
