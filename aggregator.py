#!/usr/bin/env python3
'''
aggregator.py
This script aggregates per-read per-nucleotide statistics over user-specified regions.

Written for the Kim Lab (August 10, 2021)

See the README file for documentation.

Chris Kimmel
chris.kimmel@live.com
'''

################################################################################
############################# IMPORTS AND PRAGMAS ##############################
################################################################################

# pylint: disable=invalid-name

import argparse
# import pandas later, after the command-line parses correctly


################################################################################
############################ COMMAND-LINE INTERFACE ############################
################################################################################

# Create parser and argument groups

text = 'Aggregate per-nucleotide statistics over noncontiguous genomic regions'
parser = argparse.ArgumentParser(description=text)

text = 'Input and output filepaths'
filepath_args = parser.add_argument_group('Filepaths', description=text)

text = 'Column names in TO-AGGREGATE csv file'
to_aggregate_args = parser.add_argument_group('TO-AGGREGATE',
    description=text)

text = 'Column names in REGIONS csv file'
regions_args = parser.add_argument_group('REGIONS',
    description=text)

# text = 'Column names in OUTPUT'
# output_args = parser.add_argument_group('OUTPUT column names',
#     description=text)


# filepath_args

text = 'Filepath to CSV file containing the statistics to aggregate'
filepath_args.add_argument('to_aggregate', metavar='TO-AGGREGATE', help=text)

text = 'Filepath to CSV file describing the genomic regions over which to '\
    'aggregate'
filepath_args.add_argument('regions', metavar='REGIONS', help=text)

test = 'Filepath to the output file (will be overwritten if alread exists)'
filepath_args.add_argument('output_filepath', metavar='OUTPUT', help=text,
    default='out.csv')


# to_aggregate_args

text = 'Genomic position index in TO-AGGREGATE'
to_aggregate_args.add_argument('--pos-to-aggregate', metavar='COLNAME',
    default='pos_0b', help=text)

text = 'Statistic in TO-AGGREGATE over which to aggregate (also used as '\
    'column-name in OUTPUT'
to_aggregate_args.add_argument('--stat', metavar='COLNAME', default='stat',
    help=text)

text = 'Coverage-depth column in TO-AGGREGATE'
to_aggregate_args.add_argument('--covg', metavar='COLNAME', default='covg',
    help=text)


# region_args

text = 'Column in REGIONS containing region names (also used as a column-name '\
    'in OUTPUT)'
regions_args.add_argument('--region', metavar='COLNAME', default='region',
    help=text)

text = 'Genomic position column in REGIONS'
regions_args.add_argument('--pos-regions', metavar='COLNAME', default='pos_0b',
    help=text)


################################################################################
################################## PARSE ARGS ##################################
################################################################################

args = parser.parse_args()
region_cols = list(args.region.split(','))
import pandas as pd # pylint: disable=wrong-import-position


################################################################################
################################# DATA IMPORT ##################################
################################################################################

to_aggregate = pd.read_csv(args.to_aggregate)
regions = pd.read_csv(args.regions)


################################################################################
################################ MERGE DATASETS ################################
################################################################################

merged = to_aggregate.merge(
    regions,
    how='inner',
    left_on=args.pos_to_aggregate,
    right_on=args.pos_regions,
    validate='one_to_many',
)
del to_aggregate
del regions


################################################################################
############################# AGGREGATE STATISTICS #############################
################################################################################

(
    merged
    .assign(weighted_term_=lambda x: x[args.stat] * x[args.covg])
    .groupby(region_cols)
    .agg(
        sum_weight_=(args.covg, sum),
        sum_weighted_term_=('weighted_term_', sum),
    )
    .reset_index()
    .assign(**{args.stat:lambda x: x['sum_weighted_term_'] / x['sum_weight_']})
    .loc[:, region_cols + [args.stat]]
    .to_csv(args.output_filepath, index=False)
)
