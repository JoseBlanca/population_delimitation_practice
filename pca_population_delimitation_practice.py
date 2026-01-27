import marimo

__generated_with = "0.19.6"
app = marimo.App(width="medium")


@app.cell
def _():
    from pathlib import Path

    import marimo as mo
    import pandas
    import numpy
    import scatter3d

    PROJECT_DIR = Path(__file__).parent
    DATA_DIR = PROJECT_DIR / "data"
    PASSPORTS = DATA_DIR / 'tomato_passports.csv'
    PCA_RESULT = DATA_DIR / 'tomato_pca.csv'
    return PASSPORTS, PCA_RESULT, mo, numpy, pandas, scatter3d


@app.cell
def _(mo):
    mo.md(r"""
    # Population delimitation practice
    """)
    return


@app.cell
def _(PASSPORTS, pandas):
    passports = pandas.read_csv(PASSPORTS, index_col='id')
    passports
    return (passports,)


@app.cell
def _(PCA_RESULT, pandas):
    pca_res = pandas.read_csv(PCA_RESULT, index_col='id')
    pca_res
    return (pca_res,)


@app.cell
def _(numpy, pandas, passports, pca_res, scatter3d):
    xyz = pca_res.iloc[:, :3]
    data = pandas.merge(xyz, passports.loc[:, ('Taxon', 'Country')], left_index=True, right_index=True, how="left")
    taxa = scatter3d.Category(data.loc[:, 'Taxon'])
    country = scatter3d.Category(data.loc[:, 'Country'])
    populations = scatter3d.Category(pandas.Series(numpy.full((data.shape[0], ), 'unclass'), index=data.index))
    populations.set_label_list(['unclass', 'pop1', 'pop2', 'pop3', 'pop4', 'pop5'])

    widget = scatter3d.Scatter3dWidget(data.iloc[:, :3].to_numpy(), category=populations)
    widget
    return (populations,)


@app.cell
def _(populations):
    from collections import Counter
    print(Counter(populations.values))
    return


if __name__ == "__main__":
    app.run()
