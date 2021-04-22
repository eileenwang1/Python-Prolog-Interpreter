```prolog
0. sibling(X, Y) :- parent_child(Z, X), parent_child(Z, Y).
1. parent_child( tom_smith, mary ).
2. parent_child( tom_smith, jack ).

?- sibling(mary,X).
X = [mary,jack].
```
## Proof for sibling(mary,mary)
rewrite of rule 0 <br />
```1. parent_child(Z, X), parent_child(Z, Y) -> sibling(X,Y)``` <br />
from step 1, by universal elimination, we assign Z:=tom_smith,X:=mary <br />
```2. parent_child(tom_smith,mary),parent_child(tom_smith,Y) -> sibling(mary,Y)```<br />
from step 2, by universal elimination, we assign Y:=mary<br />
```3. parent_child(tom_smith,mary),parent_child(tom_smith,mary) -> sibling(mary,mary)```<br />
by rule 1, we have <br />
```4. parent_child( tom_smith, mary ).```<br />
from step 4, by conjunction intro, <br />
```5. parent_child( tom_smith, mary ), parent_child( tom_smith, mary )```<br />
from step 3 and 5, by conditional elimination,<br />
```6. sibling(mary,mary)```<br />

## Proof for sibling(mary,jack)
rewrite of rule 0 <br />
```1. parent_child(Z, X), parent_child(Z, Y) -> sibling(X,Y)``` <br />
from step 1, by universal elimination, we assign Z:=tom_smith,X:=mary <br />
```2. parent_child(tom_smith,mary),parent_child(tom_smith,Y) -> sibling(mary,Y)``` <br />
from step 2, by universal elimination, we assign Y:=mary <br />
```3. parent_child(tom_smith,mary),parent_child(tom_smith,mary) -> sibling(mary,mary)``` <br />
by rule 1, we have <br />
```4. parent_child( tom_smith, mary ).```<br />
by rule 2, we have <br />
```5. parent_child( tom_smith, jack ).```<br />
from step 4 and 5, by conjunction intro, <br />
```6. parent_child( tom_smith, mary ), parent_child( tom_smith, jack )```<br />
from step 3 and 6, by conditional elimination,<br />
```7. sibling(mary,jack)```<br />
