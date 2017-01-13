# Dance Partner Assignment

#### James Diao, 11 January 2017

Implementing the Hungarian (Munkres) algorithm for assigning dance partners by minimizing a summed cost function. 


-------------------------------------------------------------

### METHOD DESCRIPTION

In the simplest terms, the match works like this:  
<br />
1. Let there by L leaders and F followers.  
2. All leaders rank their desired followers from 1-F, and all followers rank their desired leaders from 1-L.  
This information is all entered into an LxF matrix, and an FxL matrix, respectively.  
3. All possible ballroom partnerships are assigned a score, or "cost."  
This cost is a function of the two preferences: the preference of the leader (L), and the preference of the follower (F).  
For example, let's say Andrew ranks Alyssa 4/10 and Alyssa ranks Andrew 2/8, and the cost function is L^2 + F^2.  
In that case, the "cost" of the partnership is 4^2 + 2^2 = 20. The lower the cost, the more ideal the match.  
4. The algorithm finds the set of all matches that minimize the overall cost.  
<br />
The repo contains sample input and output data, which should give you an clearer idea of how it works. 
<br />
For more technical details, see: https://en.wikipedia.org/wiki/Hungarian_algorithm


Why don't we use the stable match algorithm?  
Stable match strongly favors one group over the other, in a way that cannot be tuned the way a cost function can.  
In trying it out with sample data, I would often see a leader get their 1st choice, but as a follower's 8th choice.  
Moreover, it is also annoying to implement with unequal numbers of leaders and followers. 


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
 - The default is C(L,F) = L^2 + F^2.  
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


