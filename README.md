# Dance Partner Assignment

#### James Diao, 11 January 2017

Implementing the Hungarian (Munkres) algorithm for assigning dance partners by minimizing a summed cost function. 


-------------------------------------------------------------

### CLONE REPOS

1. Clone this source repository: <br />
 - `$ git clone https://github.com/jamesdiao/Dance-Partner-Assignment.git`  
2. Clone the Munkres package for Python:  
 - `$ git clone https://github.com/bmc/munkres.git`

-------------------------------------------------------------

### RUNNING THE SCRIPT

1. Install the munkres package by running:  
 - `$ python setup.py install`  
2. Edit `leader_matrix.csv` and `follower_matrix.csv` with the correct names and values in the same format.  
3. Define a cost function in python language and write this as a single line in `cost_function.txt`.  
 - C(L,F) is a function of L (the leader's ranking of the follower) and F (the follower's ranking of the leader).  
 - The default is $C(L,F) = L^2 + F^2$.  
 - We suggest giving additional weight the smaller group (e.g., if there are fewer leaders, weight the leader preferences higher).  
4. Run `Partner_Assignment.py` with:  
 - `$ python Partner_Assignment.py`
5. OR, make the `Partner_Assignment.py` executable and run it directly:  
 - `$ chmod +x Partner_Assignment.py`
 - `$ ./Partner_Assignment.py`  

Final partner assignments will be given in `match_outputs.csv`, along with individual couple penalties and the total cost at the bottom. 

-----------------------------------------------------------------

### CONTACT  

Please contact James Diao (james.diao@yale.edu) with any questions. 

<br />
<br />
<br />


