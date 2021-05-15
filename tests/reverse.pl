reverse1([],[]).
reverse1([X|XS],Rev) :- reverse1(XS,Revs), append(Revs,[X],Rev).
