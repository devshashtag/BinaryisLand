# Binary island
Finding large island in Binary Map


## DESCRIPTION
**=>** one map : row x column

**=>** all zero numbers are water

**=>** all one numbers are land

## RULES

**Any land(1) can be connected to another land(1) and made an island.**

if they are in range:

```
1 1 1
1 x 1
1 1 1
```

## Example

```
0000000000
0100101000
0101111010
0101011100
0000000000
```

*The lands are connected and make two islands*:

```

 1  1 1
 | /|\|
 1 1111  1
 | |/\|\/
 1 1 111

```


## TARGETS

**Find the largest island**

**this algorithm help us to find**:

1 - **largest island**

2 - **size all islands**

3 - **categorize islands**

with grouping lands we can find largest island

## screenshots

![alt text](https://raw.githubusercontent.com/unprogramable/BinaryisLand/master/screenshots/solve1.png)

![alt text](https://raw.githubusercontent.com/unprogramable/BinaryisLand/master/screenshots/solve3.png)

![alt text](https://raw.githubusercontent.com/unprogramable/BinaryisLand/master/screenshots/solve4.png)

![alt text](https://raw.githubusercontent.com/unprogramable/BinaryisLand/master/screenshots/solve5.png)

![alt text](https://raw.githubusercontent.com/unprogramable/BinaryisLand/master/screenshots/solve3.png)