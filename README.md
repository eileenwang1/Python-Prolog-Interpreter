

# Python Prolog Proof Constructor
This project trackes the search tree that the python prolog interpreter searches for solutions. From the search tree, it construct a proof tree and a formal proof for each step of the search.
## Sample Prolog Program
```prolog
great_grand_parent(A,D) :- parent(A,B),grand_parent(B,D).
grand_parent(A,C) :- parent(A,B), parent(B,C).
parent(alice,bob).
parent(bob,charlie).
parent(charlie,daisy).

great_grand_parent(X,daisy).
```
## Search Tree
![](/images/test5_plot.png)

## Proof Tree
![](/images/test5_tree4.png)
## Formal Proof

```
NODE 4
0    parent(A,B) ∧ grand_parent(B,D) -> great_grand_parent(A,D)       	    P
1    parent(A,B) ∧ parent(B,C) -> grand_parent(A,C)                   	    P
2    parent(alice,bob)                                                	    P
3    parent(bob,charlie)                                              	    P
4    parent(charlie,daisy)                                            	    P
     ---------------
5    parent(alice,bob)                                                	    2
6    parent(bob,charlie)                                              	    3
7    parent(charlie,daisy)                                            	    4
8    parent(bob,charlie) ∧ parent(charlie,daisy)                      	6,7 ∧ Intro
9    parent(bob,charlie) ∧ parent(charlie,daisy) -> grand_parent(bob,daisy)	 1 UI
10   grand_parent(bob,daisy)                                          	8,9 -> Elim
11   parent(alice,bob) ∧ grand_parent(bob,daisy)                      	5,10 ∧ Intro
12   parent(alice,bob) ∧ grand_parent(bob,daisy) -> great_grand_parent(alice,daisy)	 0 UI
13   great_grand_parent(alice,daisy)   
```
## Dependencies
 * igraph
 * Cairo (from homebrew)
 


## Next steps:
 * readability for graph plots (orientation, position of labels, etc.)


<!--- # April 9 Update
limitation: does not support recursion.
 -->
