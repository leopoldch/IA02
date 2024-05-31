tete([T|_], T).
reste([_|R],R).
vide([]).

element(X,[X|_]).
element(Y,[X|L]) :- X \== Y, element(Y,L).

dernier([X],X).
dernier([Y|L],X) :- Y \== X, dernier(L,X).

longueur([],0).
longueur([_|Y],L) :- longueur(Y,L2),L is L2+1.

nombre([],X,0).
nombre([X|T],X,Y):- nombre(T,X,N), Y is 1+N.
nombre([X1|T],X,N):- X1\=X,nombre(T,X,N).

concat([], L, L).
concat([T|R], L2, [T|LTmp]) :- concat(R, L2, LTmp).

inverse([],[]). 
inverse([X|L1],L2) :- inverse(L1,L3),append(L3,[X],L2). % append est implémenté de base

% sous liste présente ou non ? 
sous_liste(L1,[]).
sous_liste(L1,[_|L2]).
sous_liste(L1,L2):-sous_liste(L1,L2).

% retirer un élément d'une liste et mettre la nouvelle liste dans R 
retire_element(L, X, R):-