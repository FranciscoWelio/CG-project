# Projeto de Computação Gráfica

Neste projeto de computação gráfica, abordaremos as principais técnicas e algoritmos para a geração de primitivas gráficas básicas, como retas, circunferências e elipses, bem como as transformações 2D que podem ser aplicadas a essas figuras. Esses conceitos são fundamentais para o desenvolvimento de gráficos computacionais, animações e simulações.

## Algoritmos de Geração de Retas

### 1. **Algoritmo DDA (Digital Differential Analyzer)**
O DDA é um algoritmo incremental utilizado para traçar retas entre dois pontos. Ele funciona calculando o valor de incremento de \(x\) e \(y\) com base na diferença entre as coordenadas dos pontos inicial e final.

Passos do algoritmo:
- Determina-se o maior deslocamento entre as coordenadas \(x\) e \(y\) (delta X e delta Y).
- Inicia-se no ponto inicial e incrementa-se, ponto a ponto, de acordo com a maior diferença entre as coordenadas.

Fórmulas básicas:
- \(\Delta x = x_2 - x_1\)
- \(\Delta y = y_2 - y_1\)
- Se \(\Delta x > \Delta y\), incrementa-se \(x\) e calcula-se \(y\) correspondente, e vice-versa.

### 2. **Algoritmo do Ponto Médio**
O algoritmo do ponto médio (ou Bresenham) é mais eficiente que o DDA, pois trabalha apenas com aritmética inteira, eliminando a necessidade de cálculos de ponto flutuante.

Passos do algoritmo:
- Começa-se com o ponto inicial da reta e calcula-se a diferença dos deltas entre \(x\) e \(y\).
- O ponto médio entre dois pixels adjacentes é usado para determinar o próximo ponto a ser plotado.
- O algoritmo decide, a cada passo, qual pixel está mais próximo da reta verdadeira e avança de acordo.

Fórmulas básicas:
- Um termo de decisão \(d = \Delta y - \frac{\Delta x}{2}\) é utilizado para determinar qual ponto é plotado.

## Algoritmos de Geração de Circunferências

### 1. **Equação Explícita**
A equação geral da circunferência com centro em \( (x_0, y_0) \) e raio \(r\) é:
\[
(x - x_0)^2 + (y - y_0)^2 = r^2
\]
Essa fórmula permite calcular \(y\) diretamente para um dado valor de \(x\). Porém, seu uso direto em computação gráfica não é eficiente devido aos cálculos de raízes quadradas.

### 2. **Método Trigonométrico**
Neste método, a circunferência é desenhada utilizando funções trigonométricas:
\[
x = x_0 + r \cos(\theta)
\]
\[
y = y_0 + r \sin(\theta)
\]
Variando o ângulo \(\theta\) de 0 a \(2\pi\), podemos plotar todos os pontos da circunferência. Contudo, cálculos trigonométricos podem ser computacionalmente caros.

### 3. **Algoritmo do Ponto Médio**
Assim como para retas, o algoritmo do ponto médio pode ser adaptado para circunferências. Ele aproveita a simetria dos octantes para reduzir o número de cálculos e traçar a circunferência com aritmética inteira.

## Algoritmo de Geração de Elipses

A equação geral da elipse com centro em \( (x_0, y_0) \), semi-eixos \(a\) e \(b\) é:
\[
\frac{(x - x_0)^2}{a^2} + \frac{(y - y_0)^2}{b^2} = 1
\]
Existem também variações do algoritmo do ponto médio que podem ser aplicadas para desenhar elipses, aproveitando sua simetria e minimizando cálculos de ponto flutuante.

## Transformações 2D com Matrizes Homogêneas

Nas transformações 2D, o uso de **matrizes homogêneas** facilita a composição de várias transformações em uma única operação. Para representar um ponto \([x, y]\), utilizamos a forma homogênea \([x, y, 1]\), o que permite que todas as transformações geométricas possam ser feitas através de multiplicações de matrizes.

### 1. **Translação**
A translação move um objeto ao somar valores constantes \(t_x\) e \(t_y\) às coordenadas \(x\) e \(y\). A matriz homogênea para a translação é:

\[
T(t_x, t_y) =
\begin{bmatrix}
1 & 0 & t_x \\
0 & 1 & t_y \\
0 & 0 & 1
\end{bmatrix}
\]

Multiplicando esta matriz por um ponto \([x, y, 1]\), obtemos o novo ponto transladado \([x', y', 1]\):

\[
\begin{bmatrix}
1 & 0 & t_x \\
0 & 1 & t_y \\
0 & 0 & 1
\end{bmatrix}
\begin{bmatrix}
x \\
y \\
1
\end{bmatrix}
=
\begin{bmatrix}
x + t_x \\
y + t_y \\
1
\end{bmatrix}
\]

### 2. **Escala**
A escala altera o tamanho de um objeto, multiplicando suas coordenadas por um fator \(s_x\) e \(s_y\). A matriz homogênea para a escala é:

\[
S(s_x, s_y) =
\begin{bmatrix}
s_x & 0 & 0 \\
0 & s_y & 0 \\
0 & 0 & 1
\end{bmatrix}
\]

Multiplicando a matriz de escala por um ponto \([x, y, 1]\), obtemos o ponto escalado \([x', y', 1]\):

\[
\begin{bmatrix}
s_x & 0 & 0 \\
0 & s_y & 0 \\
0 & 0 & 1
\end{bmatrix}
\begin{bmatrix}
x \\
y \\
1
\end{bmatrix}
=
\begin{bmatrix}
x \cdot s_x \\
y \cdot s_y \\
1
\end{bmatrix}
\]

### 3. **Rotação**
A rotação gira um objeto em torno de um ponto, geralmente a origem, de acordo com um ângulo \(\theta\). A matriz homogênea para a rotação é:

\[
R(\theta) =
\begin{bmatrix}
\cos(\theta) & -\sin(\theta) & 0 \\
\sin(\theta) & \cos(\theta) & 0 \\
0 & 0 & 1
\end{bmatrix}
\]

Multiplicando a matriz de rotação por um ponto \([x, y, 1]\), obtemos o novo ponto rotacionado \([x', y', 1]\):

\[
\begin{bmatrix}
\cos(\theta) & -\sin(\theta) & 0 \\
\sin(\theta) & \cos(\theta) & 0 \\
0 & 0 & 1
\end{bmatrix}
\begin{bmatrix}
x \\
y \\
1
\end{bmatrix}
=
\begin{bmatrix}
x \cos(\theta) - y \sin(\theta) \\
x \sin(\theta) + y \cos(\theta) \\
1
\end{bmatrix}
\]

### 4. **Reflexão**
A reflexão inverte as coordenadas de um objeto em relação a um eixo. A matriz homogênea para refletir em torno do eixo \(x\) é:

\[
\text{Reflexão no eixo } x =
\begin{bmatrix}
1 & 0 & 0 \\
0 & -1 & 0 \\
0 & 0 & 1
\end{bmatrix}
\]

Para refletir em torno do eixo \(y\), a matriz é:

\[
\text{Reflexão no eixo } y =
\begin{bmatrix}
-1 & 0 & 0 \\
0 & 1 & 0 \\
0 & 0 & 1
\end{bmatrix}
\]

### 5. **Cisalhamento**
O cisalhamento distorce um objeto, alterando suas coordenadas em uma direção proporcional à outra. A matriz homogênea para o cisalhamento no eixo \(x\) é:

\[
Sh_x(sh_x) =
\begin{bmatrix}
1 & sh_x & 0 \\
0 & 1 & 0 \\
0 & 0 & 1
\end{bmatrix}
\]

E para o cisalhamento no eixo \(y\):

\[
Sh_y(sh_y) =
\begin{bmatrix}
1 & 0 & 0 \\
sh_y & 1 & 0 \\
0 & 0 & 1
\end{bmatrix}
\]

## Conclusão

Este projeto abrange os principais algoritmos e transformações geométricas utilizados na computação gráfica. Com o uso de coordenadas homogêneas e multiplicação de matrizes, podemos unificar e simplificar a aplicação de transformações como translação, rotação, escala, reflexão e cisalhamento.
