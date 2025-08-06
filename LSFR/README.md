# Assignment 1
###### Cryptography CS 578
###### Jacob Glik
###### 09/09/2024

<br />

_________

## Question 1

###### Run `python3 question1.py`

a. Relative Ciphertext Letter Frequency:
```py
A: 150  B: 100  C: 86   F: 83   D: 76   I: 75   G: 70
E: 58   L: 50   K: 47   H: 45   J: 40   M: 37   S: 24
N: 24   Q: 23   P: 19   O: 19   R: 15   U: 15   T: 9
V: 9    Y: 3
```

b. Decrypted ciphertext:

```buildoutcfg
electrical and computer engineers develop and create products that change the world and
make our lives easier the cell phones we depend on the computers used in national
security and the electrical systems that make our cars operate were all created by
electrical and computer engineers at wpi we keep that progress moving forward with our
innovative research and out-of-the box approaches the department of electrical and
computer engineering at wpi challenges students to push themselves to understand
societys and technologys complex issues in a broader context than whats in front of
them we want our students whether they are earning an undergraduate minor or a doctorate
to tackle societys most pressing problems and uncover new ways of solving them
whether its developing systems that can locate firefighters in the middle of a
burning building or creating neuroprosthetics that look and function like natural
limbs our faculty and students are at the front edge of remarkable innovation while
advancing technologies is at our core we also take human connections very seriously
in ece we pride ourselves on the family-like atmosphere we cultivate; faculty
students and staff encourage each others every success and are there for the
challenges both in the classroom and in life
```

c. Ciphertext : plaintext - letter pairs:

```py
'A': 'e',   'M': 'u',
'B': 't',   'S': 'p',
'C': 'a',   'N': 'm',
'F': 'n',   'Q': 'g',
'D': 'o',   'P': 'f',
'I': 'r',   'O': 'w',
'G': 's',   'R': 'y',
'E': 'i',   'U': 'v',
'L': 'c',   'T': 'b',
'K': 'l',   'V': 'k',
'H': 'h',   'Y': 'x',
'J': 'd',
```

d. Plaintext letter frequency:

```py
e: 150  t: 100  a: 86   n: 83   o: 76   r: 75   s: 70
i: 58   c: 50   l: 47   h: 45   d: 40   u: 37   p: 24
m: 24   g: 23   f: 19   w: 19   y: 15   v: 15   b: 9
k: 9    x: 3
```

<br />

_________

## Question 2

###### I picked the first equation: `f(x) = (x¹⁰ + x³ + 1)`

###### Run `python3 question2.py`

###### See `LSFR_generation_table_1028.txt` for complete table. (Col "drp" is the bit that was dropped, col "clc" is the bit that was calculated, and col "dec" is the decimal value of that row.)

a. Circuit Diagrams for equation picked above:

![](Simplified%20image.jpg)
![](LFSR%20Drawing.jpg)

b. First 512 bits:

```txt
OUTPUT BIT STREAM GENERATED (size=512, col_length=64):
1000011001101101010000011101001111010011010100100111000001111100
1110011011110100010101011011111000010011101000111010111110110100
1000010000101001010110001110011111110110000100011010011100100111
1000011011101100011000111101111101001001010000001101000110010111
0100101101000100010110011010010100100011000011101101111000001011
1001010111001110111011100110011101010111011110110010100010011011
0001000011100101111100101001100110010101010011111100110001101011
1100110101101001100010010111000010111101010101011111111010000010
```


c. What is the period?

```buildoutcfg
It is 1028.
This can be calculated by 2^(number of registers i.e. 10)
This can be seen if you change the size value to anything over 1028 and copy the 
path (below) to a google doc and use `crtl+f` to highlight repeated values
```

```micro
PATH:609,816,408,716,870,435,729,364,694,347,173,86,43,21,522,773,898,449,736,368,184,604,814,919,971,485,754,377,188,606,815,407,715,357,690,345,172,598,299,149,586,805,914,457,228,114,57,28,526,775,899,961,992,496,248,636,830,927,463,231,627,825,412,718,871,947,985,492,758,379,189,94,559,279,651,325,674,337,680,852,426,725,874,949,986,1005,502,251,125,62,543,271,135,579,801,912,456,740,370,185,92,558,791,907,453,738,369,696,860,942,983,1003,501,762,893,446,735,367,183,603,301,150,75,37,530,265,132,66,33,528,264,644,322,161,592,296,660,330,677,850,425,212,106,565,794,909,454,227,625,824,924,974,999,1011,1017,508,766,895,447,223,111,55,539,269,134,67,545,784,392,708,354,177,600,812,918,459,229,626,313,156,590,807,915,969,484,242,121,60,542,783,391,707,865,944,472,748,886,443,221,110,567,795,397,198,99,561,792,908,966,483,753,888,956,990,1007,503,763,381,190,607,303,151,587,293,658,329,164,82,41,20,10,517,770,385,704,352,176,88,556,790,395,197,610,305,664,844,934,467,745,372,186,605,302,663,843,421,722,361,180,90,557,278,139,69,546,273,648,836,418,209,616,820,410,717,358,179,601,300,662,331,165,594,297,148,74,549,786,393,196,98,49,536,780,902,451,737,880,440,732,878,951,987,493,246,123,61,30,527,263,643,833,928,464,232,628,314,669,334,679,851,937,468,234,629,826,925,462,743,883,953,476,750,887,955,477,238,631,827,413,206,615,819,921,460,742,371,697,348,686,855,939,469,746,885,954,989,494,759,891,445,222,623,311,667,333,166,83,553,276,138,581,802,401,712,868,434,217,108,566,283,141,70,35,529,776,900,450,225,624,312,668,846,935,979,1001,500,250,637,318,671,335,167,595,809,404,202,613,818,409,204,614,307,665,332,678,339,681,340,170,597,810,917,970,997,1010,505,252,638,831,415,207,103,563,793,396,710,355,689,856,940,982,491,245,634,829,414,719,359,691,857,428,726,363,181,602,813,406,203,101,562,281,140,582,291,657,840,932,466,233,116,58,541,270,647,835,929,976,488,756,378,701,350,687,343,683,341,682,853,938,981,1002,1013,1018,1021,510,767,383,191,95,47,23,523,261,642,321,672,336,168,596,298,661,842,933
```

d. Encrypt P = `11101100000110111011010011111010` using the first 32 bits

```buildoutcfg
01101010011101101111010100101001
```

e. Decrypt cypher_p = `01101010011101101111010100101001` using the same first 32 bits

```buildoutcfg
11101100000110111011010011111010
```

<br />

<br />

<br />

<br />

<br />

<br />
