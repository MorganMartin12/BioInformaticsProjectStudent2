# Graphical display of newly formed telomeres

## Description
This program takes the blast output of newly found teleomers and converts it to a GFF file that will display information about the location of the newly found teleomers in the IGV browser. 

## Input
The program takes a blast output format 6, with an additional header at the top. The header gives information on the length of the chromosomes. The header is styled like this:

\# of Chromosomes
 Chromosome1;# length of chromsome
...
Blast format file

## Running the program
```
python converter.py <input_file> <output_file.gff>
```
## Example output
This is an example out put using the Eleusine-indica genome, the fasta file is provided, along with the Blast results and gff file. 


![Results](https://github.com/MorganMartin12/BioInformaticsProjectStudent2/blob/master/Results.PNG)
