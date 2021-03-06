from argparse import ArgumentParser
import pandas as pd


def main():
    args = get_args()
    df = pd.read_csv(filepath_or_buffer=args.STRs,
                     sep="\t",
                     header=0)
    df["identifier"] = df["chrom"] + ":" + df["start"].astype(str) + "-" + df["repeatunit"]
    pivot = df.pivot(index='identifier',
                     columns='sample',
                     values=['locuscoverage', 'outlier', 'p_adj', 'bpInsertion', 'repeatUnits'])
    for feature in ['locuscoverage', 'outlier', 'bpInsertion', 'repeatUnits']:
        pivot.loc[:, (feature, "max")] = pivot[feature].max(axis="columns")
    pivot.loc[:, ('p_adj', "min")] = pivot['p_adj'].min(axis="columns")

    pivot.columns = ['_'.join(col).strip() for col in pivot.columns.values]

    if args.sort == 'location':
        sorter = ["chrom", "start", "end"]
    else:
        sorter = 'p_adj_min'

    print(
        df[["identifier", "chrom", "start", "end", "repeatunit", "reflen"]]
        .drop_duplicates()
        .set_index('identifier')
        .join(pivot)
        .sort_values(sorter)
        .to_csv(sep="\t")
    )


def get_args():
    parser = ArgumentParser(description="Reformat STRetch STRs.tsv to stdout")
    parser.add_argument("STRs", help="File STRs.tsv generated by STRetch")
    parser.add_argument("--sort",
                        help="property to sort on. Default: chromosomal location",
                        choices=['location', 'pval'],
                        default='location')
    return parser.parse_args()


if __name__ == '__main__':
    main()
