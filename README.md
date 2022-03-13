# Monopoly Game

Welcome to the __654687th__ version of the <span style="color:red">**Monopoly**</span> using Python.

## Why is this one different ?

As display, I use the console (curses module), no graphic interface, but maybe later. I wanted to focus on the featuring aspect of the code. I hope you like how things are showed though. Also, I tried to make the code as dynamic as possible to.... read **What next**

## How does this game work ?

You have to choose how many players there is, then the game can start.
Basically, you do something by pressing keys, simple as that. A key always does the same thing, obviously you can't press one of them if it is not available.

| Keys | Do |
|--- |--- |
| 0 | Roll Dice |
| 1 | Mortgage |
| 2 | Unmortage |
| 3 | Build |
| 4 | Sell |
| 5 | End turn |
| 6 | Try double (only in jail) |
| 7 | Pay Fine (only in jail) |
| 8 | Use Free Jail Card (only in jail) |
| 9 | Get out of the game (bankruptcy) |
| c | Cancel a choice |
| q | Quit the game |

## Some cool features ?

Use of **Pandas** as data structure to store all tiles of the Monopoly Board  

Use of **NumPy** as data structure to store states of all properties (owned by, mortgaged, building on)

```python
own = np.zeros((10, 4, 3), dtype=int)
```
10 families  
4 properties by family (actually, 2, 3 or 4 but numpy doesn't allow it so have to choose the maximum value)  
3 different states (own, mortgage, building)
    

## Todo

AI Things

## What next ??

I would like to upgrade it. I would like to program the first ever Mega version of the Monopoly on a computer. I think nobody has done it yet.  
https://monopoly.fandom.com/wiki/Monopoly:_The_Mega_Edition

## By

Verdon Dorian  
https://www.linkedin.com/in/dorian-verdon-63a159174/