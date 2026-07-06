extends ml
tags machine_learning
date 2026-06-17

# Machine learning episode 1 - small beginnings
I think this is generally going to be a slow series. I want to learn (and explain to you) how machine learning works from first principles. To be honest, I think this might be more math heavy than I would want for a general audience, so instead I'm mostly writing this assuming you know single variable calculus. I would also be writing this in latex if I wasn't lazy. 
If you don't know single variable calculus, consider enrolling in a course for it or watching 3blue1brown's informative video series on it. 

To start, I'm going with an interesting exercise. Given some unknown function ***f***, write code to optimize it. Unfortunately, I was a fool and wrote my initial function to only cover 8 bit integers, which is a pretty small domain for functions. The code is <a href="/machine_learning/example-1-1.zig">here</a>. I wrote it using Zig, but the comments should make it pretty readable. 
To fix the fact that I wrote it to only analyze integers, here's a version <a href="/machine_learning_example-1-2.zig">that works on 126 bit floating point</a>.

Some general observations from writing these two programs:
1. Its really slow. The floating point version takes what feels like ~20sec to find the max. I didn't bother to time it, but I assume it is pretty long. 
2. It can't really confirm that this is a global max, just a local max given the points, which leads to be less effective a lot of the time with some functions. 
Thats it for today though. Tommorrow we tackle this problem with some more real machine learning techniques. 