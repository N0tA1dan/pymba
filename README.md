# Pymba

Pymba, a simple MBA obfuscator

## What is MBA Obfuscation?

MBA stands for Mixed Boolean Arithmetic. When speaking of an MBA expression we can expect to see arithmetic operators such as + and -. We would also see boolean operators like the following:
```
^ - XOR
| - OR
& - AND
~ - NOT
```

We can use transformations to "Obfuscate" an original expression. 

Here are some transformations we can do on operators. I will refer to these as transformation "rules" or substitutions. Note these substitutions can also be generated using De Morgan's Law.
```
if the operation is X & Y then apply the substitution (X + Y) - (X | Y)
if the operation is X ^ Y then apply the substitution (X | Y) - (X & Y)
if the operation is X - Y then apply the substitution (X ^ -Y) + 2*(X & -Y)
if the operation is X + Y then apply the substitution (X & Y) + (X | Y)
if the operation is X | Y then apply the substitution (~X&~Y)+((X+Y)−(~X&~Y))
```

For example if we have the arithmetic expression: 
```
A+(B^C)
```
Using the following transformations we get:
```
((A & ((B | C) - (B & C))) + (A | ((B | C) - (B & C))))
```

## Installation and Usage

Prerequisites
- python3 or above
- git

To install simply use git to clone the repository:
```
git clone https://github.com/N0tA1dan/pymba
```

After the installation you can now run pymba. To execute pymba simply run:
```
cd pymba
python3 src/main.py
```


## How does pymba work?

First we take in an arithmetic expression and parse it into an ast Tree. This is great because we can work with 2 variables or operators at a time without corrupting the expression.

For example if we are using the expression A+(B^C)
```
    +
   / \
  A   ^
     / \
    B   C
```

Now that we have an AST Tree built from the expression we can traverse it recursively to apply our substitutions.

While traversing the tree, we will only do transformations on the operator nodes aka the nodes with any boolean or arithmetic operator.

Next we apply the substitution rules that we stated before:

```
if the operation is X & Y then apply the substitution (X + Y) - (X | Y)
if the operation is X ^ Y then apply the substitution (X | Y) - (X & Y)
if the operation is X - Y then apply the substitution (X ^ -Y) + 2*(X & -Y)
if the operation is X + Y then apply the substitution (X & Y) + (X | Y)
if the operation is X | Y then apply the substitution (~X&~Y)+((X+Y)−(~X&~Y))
```

So after all the substitutions we will get an expression that looks like this

```
((A & ((B | C) - (B & C))) + (A | ((B | C) - (B & C))))
```


## Why should we use MBA obfuscation

There are many reasons why MBA is a good way to obfuscate expressions in comparison to other obfuscation techniques:

1. Human Reverse engineering - Obviously it would be tedious for anyone to try to solve an obfuscated expression by hand. This would be particularly hard when the expression is very long in size.

2. Non-Linear - For some MBA obfuscation techniques out there, many are non-linear. As we may know, non-linear functions are hard to solve by nature and may not have any real solutions to them. There is an infinite amount of ways to represent one expression, Meaning there are an infinite amount of transformations one can do to achieve MBA obfuscation. This property of being non-linear makes solving expressions extremely difficult.

3. Resistence to optimization - Currently, as of April 2024, The compilers I am using cannot optimize the expressions pymba generates. There are probably a handful of reasons why, but this is a great example on how compiler technology cannot solve these complex MBA expressions. This is actually a great benefit if you're a developer and you need to obfuscate something without worrying of your compiler completely optimizing it out.

I have linked some research papers and other projects at the end of this README. You can do your own research as well to see how MBA is a really good technique at obfuscation.

## Generating New Expressions

To generate expressions we can use something called De Morgan's Law. I linked more about De Morgan's law in the links section.

## Examples

Here are example outputs of the following Equation: A+B

Round 1:
```
((A & B) + (A | B))
```

Round 2: 
```
((((A + B) - (A | B)) & ((~A & ~B) + ((A + B) - (~A & ~B)))) + (((A + B) - (A | B)) | ((~A & ~B) + ((A + B) - (~A & ~B)))))
```

Round 3:
```
((((((((A & B) + (A | B)) ^ -((~A & ~B) + ((A + B) - (~A & ~B)))) + ((((A & B) + (A | B)) & -((~A & ~B) + ((A + B) - (~A & ~B)))) * 2)) + ((((~A + ~B) - (~A | ~B)) & ((((A & B) + (A | B)) ^ -((~A + ~B) - (~A | ~B))) + ((((A & B) + (A | B)) & -((~A + ~B) - (~A | ~B))) * 2))) + (((~A + ~B) - (~A | ~B)) | ((((A & B) + (A | B)) ^ -((~A + ~B) - (~A | ~B))) + ((((A & B) + (A | B)) & -((~A + ~B) - (~A | ~B))) * 2))))) - (((((A & B) + (A | B)) ^ -((~A & ~B) + ((A + B) - (~A & ~B)))) + ((((A & B) + (A | B)) & -((~A & ~B) + ((A + B) - (~A & ~B)))) * 2)) | ((((~A + ~B) - (~A | ~B)) & ((((A & B) + (A | B)) ^ -((~A + ~B) - (~A | ~B))) + ((((A & B) + (A | B)) & -((~A + ~B) - (~A | ~B))) * 2))) + (((~A + ~B) - (~A | ~B)) | ((((A & B) + (A | B)) ^ -((~A + ~B) - (~A | ~B))) + ((((A & B) + (A | B)) & -((~A + ~B) - (~A | ~B))) * 2)))))) & ((~((((A & B) + (A | B)) ^ -((~A & ~B) + ((A + B) - (~A & ~B)))) + ((((A & B) + (A | B)) & -((~A & ~B) + ((A + B) - (~A & ~B)))) * 2)) & ~((((~A + ~B) - (~A | ~B)) & ((((A & B) + (A | B)) ^ -((~A + ~B) - (~A | ~B))) + ((((A & B) + (A | B)) & -((~A + ~B) - (~A | ~B))) * 2))) + (((~A + ~B) - (~A | ~B)) | ((((A & B) + (A | B)) ^ -((~A + ~B) - (~A | ~B))) + ((((A & B) + (A | B)) & -((~A + ~B) - (~A | ~B))) * 2))))) + ((((((A & B) + (A | B)) ^ -((~A & ~B) + ((A + B) - (~A & ~B)))) + ((((A & B) + (A | B)) & -((~A & ~B) + ((A + B) - (~A & ~B)))) * 2)) + ((((~A + ~B) - (~A | ~B)) & ((((A & B) + (A | B)) ^ -((~A + ~B) - (~A | ~B))) + ((((A & B) + (A | B)) & -((~A + ~B) - (~A | ~B))) * 2))) + (((~A + ~B) - (~A | ~B)) | ((((A & B) + (A | B)) ^ -((~A + ~B) - (~A | ~B))) + ((((A & B) + (A | B)) & -((~A + ~B) - (~A | ~B))) * 2))))) - (~((((A & B) + (A | B)) ^ -((~A & ~B) + ((A + B) - (~A & ~B)))) + ((((A & B) + (A | B)) & -((~A & ~B) + ((A + B) - (~A & ~B)))) * 2)) & ~((((~A + ~B) - (~A | ~B)) & ((((A & B) + (A | B)) ^ -((~A + ~B) - (~A | ~B))) + ((((A & B) + (A | B)) & -((~A + ~B) - (~A | ~B))) * 2))) + (((~A + ~B) - (~A | ~B)) | ((((A & B) + (A | B)) ^ -((~A + ~B) - (~A | ~B))) + ((((A & B) + (A | B)) & -((~A + ~B) - (~A | ~B))) * 2)))))))) + (((((((A & B) + (A | B)) ^ -((~A & ~B) + ((A + B) - (~A & ~B)))) + ((((A & B) + (A | B)) & -((~A & ~B) + ((A + B) - (~A & ~B)))) * 2)) + ((((~A + ~B) - (~A | ~B)) & ((((A & B) + (A | B)) ^ -((~A + ~B) - (~A | ~B))) + ((((A & B) + (A | B)) & -((~A + ~B) - (~A | ~B))) * 2))) + (((~A + ~B) - (~A | ~B)) | ((((A & B) + (A | B)) ^ -((~A + ~B) - (~A | ~B))) + ((((A & B) + (A | B)) & -((~A + ~B) - (~A | ~B))) * 2))))) - (((((A & B) + (A | B)) ^ -((~A & ~B) + ((A + B) - (~A & ~B)))) + ((((A & B) + (A | B)) & -((~A & ~B) + ((A + B) - (~A & ~B)))) * 2)) | ((((~A + ~B) - (~A | ~B)) & ((((A & B) + (A | B)) ^ -((~A + ~B) - (~A | ~B))) + ((((A & B) + (A | B)) & -((~A + ~B) - (~A | ~B))) * 2))) + (((~A + ~B) - (~A | ~B)) | ((((A & B) + (A | B)) ^ -((~A + ~B) - (~A | ~B))) + ((((A & B) + (A | B)) & -((~A + ~B) - (~A | ~B))) * 2)))))) | ((~((((A & B) + (A | B)) ^ -((~A & ~B) + ((A + B) - (~A & ~B)))) + ((((A & B) + (A | B)) & -((~A & ~B) + ((A + B) - (~A & ~B)))) * 2)) & ~((((~A + ~B) - (~A | ~B)) & ((((A & B) + (A | B)) ^ -((~A + ~B) - (~A | ~B))) + ((((A & B) + (A | B)) & -((~A + ~B) - (~A | ~B))) * 2))) + (((~A + ~B) - (~A | ~B)) | ((((A & B) + (A | B)) ^ -((~A + ~B) - (~A | ~B))) + ((((A & B) + (A | B)) & -((~A + ~B) - (~A | ~B))) * 2))))) + ((((((A & B) + (A | B)) ^ -((~A & ~B) + ((A + B) - (~A & ~B)))) + ((((A & B) + (A | B)) & -((~A & ~B) + ((A + B) - (~A & ~B)))) * 2)) + ((((~A + ~B) - (~A | ~B)) & ((((A & B) + (A | B)) ^ -((~A + ~B) - (~A | ~B))) + ((((A & B) + (A | B)) & -((~A + ~B) - (~A | ~B))) * 2))) + (((~A + ~B) - (~A | ~B)) | ((((A & B) + (A | B)) ^ -((~A + ~B) - (~A | ~B))) + ((((A & B) + (A | B)) & -((~A + ~B) - (~A | ~B))) * 2))))) - (~((((A & B) + (A | B)) ^ -((~A & ~B) + ((A + B) - (~A & ~B)))) + ((((A & B) + (A | B)) & -((~A & ~B) + ((A + B) - (~A & ~B)))) * 2)) & ~((((~A + ~B) - (~A | ~B)) & ((((A & B) + (A | B)) ^ -((~A + ~B) - (~A | ~B))) + ((((A & B) + (A | B)) & -((~A + ~B) - (~A | ~B))) * 2))) + (((~A + ~B) - (~A | ~B)) | ((((A & B) + (A | B)) ^ -((~A + ~B) - (~A | ~B))) + ((((A & B) + (A | B)) & -((~A + ~B) - (~A | ~B))) * 2)))))))))
```
## Possible Vulnerabilities With MBA

This project is meant as a POC. There are some issues that arrise with this specific tool.

If you're using the same tranformation rules, there is a possible security risk in doing so. Lets say I'm using the expression A+B, the output of A+B will always be ((A & B) + (A | B)) if you're using the basic transformations/substitutions I have documented about. Since these rules are hard coded, someone could possibly make a tool to do the exact opposite of what it does. However one way to easily fix this is to use De Morgan's law to generate transformation rules at run time.

To securely create tranformation rules, you can implement De Morgan's law and introduce randomness to it. Generating rules at run time eliminates the risk of someone finding the rules that were used to create the expression.

## Conclusion

In conclusion, MBA obfusation is a great way to obfuscate arithmetic expressions against computers and pesky people trying to reverse your code. 

I would like to express that although it sounds good on paper, MBA obfuscation could be horrible. So I advise you to use my obfuscator cautiously.

## Links

https://www.usenix.org/system/files/sec21fall-liu-binbin.pdf

https://www.usenix.org/conference/usenixsecurity21/presentation/liu-binbin

https://par.nsf.gov/servlets/purl/10318183

https://github.com/seekbytes/pocket

https://www.cuemath.com/data/de-morgans-law/
