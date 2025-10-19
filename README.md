# Hangman AI - Python

## Instrucțiuni de rulare
Pune fișierul `input.csv` în folderul `/data`
Rulează programul din terminal:
python src/solve_hangman.py
Programul va afișa progresul fiecărui cuvânt și numărul de încercări în terminal

Ipoteze
Fiecare cuvânt din CSV este alfabetizat și poate conține diacritice

Coloanele CSV sunt: index, cuvânt mascat, cuvânt real

AI-ul nu primește feedback greșit; ghicește literele în mod automat

Format I/O
Input: CSV cu 3 coloane (index, cuvânt mascat, cuvânt real)

Output: în terminal, pentru fiecare cuvânt: progresul, litere ghicite, poziții și numărul de încercări

Total: numărul total de încercări pentru toate cuvintele

Definiții
litere_folosite – lista literelor deja ghicite

afisare – lista literelor curente afișate pentru cuvânt

cuvinte_filtrate – lista cuvinte compatibile cu literele ghicite până acum

Limitări
Funcționează doar pentru cuvinte din limba română

AI-ul folosește strategii simple și poate ghici mai greu cuvinte cu litere rare sau diacritice

Nu există interfață grafică, doar terminal

Cerințe / Dependințe
Python 3.8+

Module standard: csv, random, collections

Dacă vrei, poți adăuga un requirements.txt gol sau cu # standard library pentru a indica că nu sunt module externe
