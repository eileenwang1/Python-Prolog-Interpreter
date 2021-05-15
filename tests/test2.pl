sibling(X, Y) :- parent_child(Z, X), parent_child(Z, Y).
parent_child( tom_smith, mary ).
parent_child( tom_smith, jack ).