<div class="cell markdown">

# Bare Account: simple double entry journaling liberary for python with SQLite backend

</div>

<div class="cell code" data-execution_count="4">

``` python
from bareaccount import Journal
```

</div>

<div class="cell markdown">

### Create an dataset

</div>

<div class="cell code" data-execution_count="5">

``` python
j = Journal.journal('leadger') 
```

</div>

<div class="cell markdown">

### Create an empty journal and show it

</div>

<div class="cell code" data-execution_count="16">

``` python
account = j.createJournal('myjournal',drop=False)
j.show(account)
```

<div class="output stream stdout">

    Journal 'myjournal' Created.

</div>

<div class="output execute_result" data-execution_count="16">

    Empty DataFrame
    Columns: [ID, credit, debit, balance]
    Index: []

</div>

</div>

<div class="cell markdown">

### Create a transaction and show the journal

</div>

<div class="cell code" data-execution_count="17">

``` python
j.transaction(account,12,2)
j.show(account)
```

<div class="output execute_result" data-execution_count="17">

``` 
   ID  credit  debit  balance
0   1    12.0    2.0     10.0
```

</div>

</div>

<div class="cell markdown">

### get balance of journal

</div>

<div class="cell code" data-execution_count="18">

``` python
# insert transactions into the journal
import random
for i in range(5):
    debit = random.randint(1,100)   
    credit = random.randint(1,100)
    j.transaction(account,credit,0)
    j.transaction(account,0,debit)

j.show(account)
```

<div class="output execute_result" data-execution_count="18">

``` 
    ID  credit  debit  balance
0    1    12.0    2.0     10.0
1    2    19.0    0.0     29.0
2    3     0.0   60.0    -31.0
3    4    40.0    0.0      9.0
4    5     0.0   84.0    -75.0
5    6    82.0    0.0      7.0
6    7     0.0    4.0      3.0
7    8    31.0    0.0     34.0
8    9     0.0    5.0     29.0
9   10    37.0    0.0     66.0
10  11     0.0   39.0     27.0
```

</div>

</div>

<div class="cell code" data-execution_count="19">

``` python
j.getbalance(account)
```

<div class="output execute_result" data-execution_count="19">

    27.0

</div>

</div>

<div class="cell markdown">

### list accounting journals

</div>

<div class="cell code" data-execution_count="20">

``` python
print(j.listJournals())
```

<div class="output stream stdout">

    ['myjournal']

</div>

</div>

<div class="cell code" data-execution_count="15">

``` python
[j.deleteJournal(x) for x in j.listJournals()]
```

<div class="output stream stdout">

    Journal 'myjournal' deleted.

</div>

<div class="output execute_result" data-execution_count="15">

    [None]

</div>

</div>
