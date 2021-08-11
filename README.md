# Aggregator

> Chris Kimmel - Aug 11, 2021 - chris.kimmel@live.com

This code aggregates per-nucleotide statistics over regions of a genome. It was
written for the Kim Lab at the Ohio State College of Veterinary Medicine.

This README file probably won't make sense to people outside our lab.


## Use-case

The use-case of this script is best explained through examples.
- Suppose you had already calculated, at each position on the genome, the
  fraction of reads with p-values below 0.40. You wish to aggregate this data
over some genomic regions. One region may be the set of all "A" nucleotides.
Another may be the set of all "DRACH"-motif nucleotides.
- Suppose you used a machine-learning model to score every position on every
  read in the genome as modified or unmodified. You have already calculated the
fraction of reads labeled modfied at each position, and you wish to aggregate
this data over a genomic region.

In both examples, the user has
1. One number for every nucleotide position on the genome (or on some portion of
   the genome)
2. A list of regions (such as the set of all A nucleotides or the set of all
DRACH-motif nucleotides)


### What this code does

This code "aggregates" statistics over a region by averaging them. The average
is weighted by coverage depth.


## Download

To download this script, run:
```bash
curl https://raw.githubusercontent.com/Chris-Kimmel/aggregator/master/aggregator.py > aggregator.py && chmod +x aggregator.py
```


## Run

### Environment

The only external library on which this script relies is Pandas. I'm using v1.2.0.


### Input Data

You need two CSV files.

1. The first input CSV file is called `to-aggregate` in the command-line
interface. It must have at least these three columns:
    - an index of nucleotide position
    - the statistic to aggregate
    - the coverage depth

2. The second CSV file the user needs is called `regions` in the command-line
interface. It needs at least two columns:
    - region names
    - nucleotide positions

In either case, the user must specify column names when running the script. It's
okay if the input CSV files have additional columns beside those required.

If the two input CSV files have any column names in common, the code may
misbehave.
