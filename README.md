# Programming-Assignment-1-Matching-and-Verifying

### Kevin Jin, 24470226
### Keerat Kohli, 41823869

To run our code, run from main.py in the src folder.

Upon running, user will be prompted to select either "matcher" or "verifier" mode. Please type the desired mode exactly as it appears to select. 

## Matcher Mode
In "matcher" mode, the program will expect the input to be in the input.in file in the data folder. This input is expected to be in the format:

-   First line: integer n, number of hospitals/students.
-   Next n lines: hospital preference lists.
-   Next n lines: student preference lists.

For example, the input file below is valid:

3  
1 2 3  
2 3 1  
2 1 3  
2 1 3  
1 2 3  
1 2 3

The output of the valid matching will be piped to output.out in the data folder. It will be in the format of n lines where each line corresponds to a hospital-student pair where the first value is the hospital number and the second is the student number. For example, the output file below:

1 1     
2 2    
3 3          

## Verifier Mode
In "verifier" mode, the expected input is both the student/hospital preference lists in the input.in file as well as the tentative matchings output.out file both in the data folder and in the same format as described above.

The output of this mode will be piped to verifier.out. It will be "VALID STABLE" if the given matching is valid. If not then the output will be "INVALID" or "UNSTABLE" with the corresponding reason why provided.

## Scalability
For the matching engine, we see that runtime scales quadratically with input size. This makes sense and matches theoretical results. The graph is displayed below.

![Matching Engine]("data\runtime_graph.png")

Similarly, the verification also takes quadratic time to run with respect to input size. The graph is displayed below.

![Verifier]("data\verifier_graph.png")
