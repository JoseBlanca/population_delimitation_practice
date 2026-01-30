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
    import plotly.express as px

    PROJECT_DIR = Path(__file__).parent
    DATA_DIR = PROJECT_DIR / "data"
    PASSPORTS = DATA_DIR / "tomato_passports.csv"
    PCA_RESULT = DATA_DIR / "tomato_pca.csv"
    return PASSPORTS, PCA_RESULT, mo, numpy, pandas, px, scatter3d


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Population delimitation practice
    """)
    return


@app.cell
def _(PASSPORTS, pandas):
    passports = pandas.read_csv(PASSPORTS, index_col="id")
    passports["Country"] = passports["Country"].replace({"PER_N": "PER"})
    return (passports,)


@app.cell
def _(PCA_RESULT, pandas):
    pca_res = pandas.read_csv(PCA_RESULT, index_col="id")
    return (pca_res,)


@app.cell
def _(numpy, pandas, passports, pca_res, scatter3d):
    xyz = pca_res.iloc[:, :3]
    data = pandas.merge(
        xyz,
        passports.loc[:, ("Taxon", "Country")],
        left_index=True,
        right_index=True,
        how="left",
    )
    taxa = scatter3d.Category(data.loc[:, "Taxon"], editable=False)
    countries = scatter3d.Category(data.loc[:, "Country"], editable=False)
    populations = scatter3d.Category(
        pandas.Series(
            numpy.full((data.shape[0],), "unclass"),
            index=data.index,
            name="populations",
        )
    )
    populations.set_label_list(["unclass", "pop1", "pop2", "pop3", "pop4", "pop5"])
    widget = scatter3d.Scatter3dWidget(
        data.iloc[:, :3].to_numpy(), category=taxa, point_ids=list(data.index)
    )
    widget.height = 800
    return countries, populations, taxa, widget


@app.cell
def _(mo, populations):
    get_pop_tick, set_pop_tick = mo.state(0)

    sub_attr = "_scatter3d_marimo_pop_sub_id"
    if getattr(populations, sub_attr, None) is None:
        counter = {"v": 0}

        def _cb(*_a, **_k):
            counter["v"] += 1
            set_pop_tick(counter["v"])

        setattr(populations, sub_attr, populations.subscribe(_cb))
    return (get_pop_tick,)


@app.cell
def _(countries, mo, populations, taxa):
    cat_dropdown = mo.ui.dropdown(
        options={"taxa": taxa, "countries": countries, "populations": populations},
        value="taxa",
    )
    cat_dropdown
    return (cat_dropdown,)


@app.cell
def _(cat_dropdown, widget):
    widget.category = cat_dropdown.value
    return


@app.cell
def _(widget):
    widget
    return


@app.cell
def _(widget):
    print(widget.active_category)
    return


@app.cell
def _(pandas, passports):
    def count_countries_in_pop(populations, widget, pop):
        classification = pandas.Series(
            populations.values.values, index=widget.point_ids, name="population"
        )
        class_country = pandas.merge(
            classification,
            passports.loc[:, "Country"],
            left_index=True,
            right_index=True,
            how="left",
        )
        if pop == "All":
            pop_country_counts = class_country.loc[:, "Country"].value_counts()
            pop_country_counts = pandas.DataFrame(
                {"Country": pop_country_counts.index, "n": pop_country_counts}
            )
        else:
            country_counts = (
                class_country.groupby(["population", "Country"])
                .size()
                .reset_index(name="n")
            )
            pop_country_counts = country_counts[
                country_counts["population"] == pop
            ].loc[:, ("Country", "n")]
        return pop_country_counts

    def count_taxa_in_pop(populations, widget, pop):
        classification = pandas.Series(
            populations.values.values, index=widget.point_ids, name="population"
        )
        class_taxon = pandas.merge(
            classification,
            passports.loc[:, "Taxon"],
            left_index=True,
            right_index=True,
            how="left",
        )
        if pop == "All":
            pop_taxon_counts = class_taxon.loc[:, "Taxon"].value_counts()
            pop_taxon_counts = pandas.DataFrame(
                {"Taxon": pop_taxon_counts.index, "n": pop_taxon_counts}
            )
        else:
            taxon_counts = (
                class_taxon.groupby(["population", "Taxon"])
                .size()
                .reset_index(name="n")
            )
            pop_taxon_counts = taxon_counts[taxon_counts["population"] == pop].loc[
                :, ("Taxon", "n")
            ]
        return pop_taxon_counts

    return count_countries_in_pop, count_taxa_in_pop


@app.cell
def _(mo, widget):
    get_active_tick, set_active_tick = mo.state(0)

    sub_attr_active_cat = "_scatter3d_marimo_active_subscribed"
    if not getattr(widget, sub_attr_active_cat, False):
        active_cat_counter = {"v": 0}

        def _cb(change):
            # traitlets observer signature: change dict
            active_cat_counter["v"] += 1
            set_active_tick(active_cat_counter["v"])

        widget.observe(_cb, names="active_category_t")
        setattr(widget, sub_attr_active_cat, True)

    return (get_active_tick,)


@app.cell
def _(mo, widget):
    pop = widget.active_category_t or "All"
    mo.md(f"""
    ## Population composition: {pop}
    """)
    return


@app.cell
def _(
    count_countries_in_pop,
    count_taxa_in_pop,
    get_active_tick,
    get_pop_tick,
    mo,
    cat_dropdown,
    px,
    widget,
):
    # rerun when:
    # - population assignments change
    # - active category changes
    _ = get_pop_tick()
    _ = get_active_tick()

    active_category = cat_dropdown.value

    active_category_value = widget.active_category_t or "All"

    country_counts = count_countries_in_pop(
        active_category, widget, active_category_value
    )
    taxon_counts = count_taxa_in_pop(active_category, widget, active_category_value)

    taxon_pie_fig = px.pie(taxon_counts, values="n", names="Taxon")

    geo_fig = px.choropleth(
        country_counts,
        locations="Country",
        locationmode="ISO-3",
        color="n",
        color_continuous_scale="Viridis",
    )
    mo.hstack(items=[taxon_pie_fig, geo_fig], widths=[1.5, 3])
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Passports
    """)
    return


@app.cell
def _(passports):
    passports
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## PCA projections
    """)
    return


@app.cell
def _(pca_res):
    pca_res
    return


if __name__ == "__main__":
    app.run()
