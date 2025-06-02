# otracker!

Um programa **(ainda em desenvolvimento)** para facilitar analisar a performance de um jogador de [osu!](https://osu.ppy.sh/) de acordo com o passar do tempo.

## uso:

vá no site do osu e crie uma porrinha dessas dai:

![image](https://github.com/user-attachments/assets/107e8d04-ba24-42d7-9d51-c36b83019db1)

então coloque o ID e senha no arquivo "app.txt". ID na primeira linha e senha na segunda. Na terceira, coloque o seu Nick usado no jogo:

```python
ID #o bglh numérico
SENHA #o texto grande
NOME #seu nick...
```
<br><br>
Ao abrir o arquivo .py, espere um pouco para que suas plays do dia sejam coletadas. Uma seta " --> " aparecerá logo em seguida.<br>
Ao digitar "playst" (plays today), suas jogadas serão listadas.<br>
Ao digitar "grapht" (graph today), serão listados em um gráfico de barras horizontais seus valores "ss" diários. (quanto maior, melhor) <br>


## ⚠️⚠️importante:


é preciso baixar essas coisas:
```
pip install ossapi
pip install aiohttp
```
alternativamente, use [esse ](https://pypi.org/project/ossapi/#files) e [esse link](https://pypi.org/project/aiohttp/#files) para baixar os bglh (respectivo ao trecho acima).

#### Não fica spammando a API, é contra os [[termos de uso]](https://osu.ppy.sh/docs/#terms-of-use) ; [[mais info ossapi]](https://github.com/tybug/ossapi)
#### A api do joguinho pode demorar pra responder tbm..
