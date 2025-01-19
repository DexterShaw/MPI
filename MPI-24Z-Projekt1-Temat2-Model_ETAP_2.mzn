include "MPI-24Z-Projekt1-Temat2-Dane_ETAP_2.dzn";

int: V_; % Liczba lokalizacji
int: N; % Maksymalna liczba serwerów na lokalizację
int: M_; % Liczba filmów
int: CTR; % Koszt transmisji 1 MB/km

set of int: V = 1..V_; % Zbiór lokalizacji serwerów
set of int: S = 1..N; % Zbiór serwerów w lokalizacji
set of int: M = 1..M_; % Zbiór filmów

array[V,S] of int: capacity; % Maksymalna liczba jednoczesnych streamów per serwer
array[V,S] of float: availability; % Prawdopodobieństwo dostępności serwera

array[M] of int: HS; % Rozmiar filmów [MB]
array[M] of int: HB; % Bitrate filmów [MB/s]
array[V,M] of int: HP; % Popularność filmów na serwerach [żądania/s]
array[M] of float: abandon_prob; % Prawdopodobieństwo porzucenia filmu

array[V,V] of int: ED; % Odległości między serwerami [km]
array[V,M] of int: CA; % Koszt alokacji filmu na serwerze

% Zmienne decyzyjne
array[V,S,M] of var 0..1: x; % 1 jeśli film m jest na serwerze s w lokalizacji v
array[V,V,M] of var 0..9999: y; % Przepływ danych filmu m między serwerami

% Ograniczenia
constraint forall(m in M)(sum(v in V, s in S)(x[v,s,m]) >= 1); % Każdy film musi być na co najmniej jednym serwerze

constraint forall(v in V, s in S)(
    sum(m in M)(x[v,s,m] * HS[m]) <= capacity[v,s]
); % Ograniczenie pojemności serwerów

constraint forall(v1 in V, v2 in V, m in M)(
    sum(s in S)(y[v1,v2,m]) * HB[m] <= sum(s in S)(capacity[v1,s])
); % Ograniczenie przepustowości

constraint forall(v in V, s in S, m in M)(
    sum(v2 in V)(y[v,v2,m]) <= availability[v,s] * capacity[v,s]
); % Uwzględnienie dostępności serwerów

% Funkcja celu: minimalizacja kosztów transmisji i alokacji, uwzględniając porzucenia
var int: allocation_cost = sum(v in V, s in S, m in M)(x[v,s,m] * CA[v,m]);
var int: transmission_cost = sum(v1 in V, v2 in V, m in M)(y[v1,v2,m] * ED[v1,v2] * HB[m] * CTR);
var float: abandonment_penalty = sum(m in M, v in V, s in S)(int2float(x[v,s,m]) * abandon_prob[m] * int2float(capacity[v,s]));


solve minimize allocation_cost + transmission_cost + abandonment_penalty;

% Output
output [
  "Koszt alokacji: " ++ show(allocation_cost) ++ "\n" ++
  "Koszt transmisji: " ++ show(transmission_cost) ++ "\n" ++
  "Kara za porzucenia: " ++ show(abandonment_penalty) ++ "\n" ++
  "Rozmieszczenie filmów:\n" ++
  concat([show(v) ++ " " ++ show(s) ++ " " ++ show(m) ++ " " ++ show(x[v,s,m]) ++ "\n" | v in V, s in S, m in M]) ++
  "\nPrzepływ danych:\n" ++
  concat([show(v1) ++ "->" ++ show(v2) ++ " film " ++ show(m) ++ " " ++ show(y[v1,v2,m]) ++ "\n" | v1 in V, v2 in V, m in M])
];
  