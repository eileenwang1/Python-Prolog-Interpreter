```prolog
0. sibling(X, Y) :- parent_child(Z, X), parent_child(Z, Y).
1. parent_child( tom_smith, mary ).
2. parent_child( tom_smith, jack ).

?- sibling(mary,X).
X = [mary,jack].
```
## Proof for sibling(mary,mary)
rewrite of rule 0
```1. parent_child(Z, X), parent_child(Z, Y) -> sibling(X,Y)``` 
from step 1, by universal elimination, we assign Z:=tom_smith,X:=mary
```2. parent_child(tom_smith,mary),parent_child(tom_smith,Y) -> sibling(mary,Y)```
from step 2, by universal elimination, we assign Y:=mary
```3. parent_child(tom_smith,mary),parent_child(tom_smith,mary) -> sibling(mary,mary)```
by rule 1, we have 
```4. parent_child( tom_smith, mary ).```
from step 4, by conjunction intro, 
```5. parent_child( tom_smith, mary ), parent_child( tom_smith, mary )```
from step 3 and 5, by conditional elimination,
```6. sibling(mary,mary)```

## Proof for sibling(mary,jack)
rewrite of rule 0
```1. parent_child(Z, X), parent_child(Z, Y) -> sibling(X,Y)``` 
from step 1, by universal elimination, we assign Z:=tom_smith,X:=mary
```2. parent_child(tom_smith,mary),parent_child(tom_smith,Y) -> sibling(mary,Y)```
from step 2, by universal elimination, we assign Y:=mary
```3. parent_child(tom_smith,mary),parent_child(tom_smith,mary) -> sibling(mary,mary)```
by rule 1, we have 
```4. parent_child( tom_smith, mary ).```
by rule 2, we have 
```5. parent_child( tom_smith, jack ).```
from step 4 and 5, by conjunction intro, 
```6. parent_child( tom_smith, mary ), parent_child( tom_smith, jack )```
from step 3 and 6, by conditional elimination,
```7. sibling(mary,jack)```
