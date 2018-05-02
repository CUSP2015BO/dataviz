import json
import altair as alt
import pandas as pd

def createChart(data, name=''):
    color_expression    = "highlight._vgsid_==datum._vgsid_"
    color_condition     = alt.ConditionalPredicateValueDef(color_expression, "SteelBlue")
    highlight_selection = alt.selection_single(name="highlight", empty="all", on="mouseover")


    barMean = alt.Chart() \
        .mark_bar(stroke="Black") \
        .encode(
            alt.X("rating:Q", axis=alt.Axis(title="The number of restaurants")),
            alt.Y('name:O', axis=alt.Axis(title="Cuisines".format(name)),
                  sort=alt.SortField(field="rating", op="mean", order='descending')),
            alt.ColorValue("LightGrey", condition=color_condition),
        ).properties(
            selection = highlight_selection,
        )

    return alt.hconcat(barMean,
        data=data,
        title="The number of restaurants ({} in NYC) - Top 25 cuisines".format(name)
    )

def createFakeChart(data, name=''):

    barMean = alt.Chart() \
        .mark_area() \
        .encode(
            )

    return alt.hconcat(barMean,
        data=data
    )


def loadData():
    import os
    cur_dir = os.path.dirname(__file__)

    df = json.load(open(os.path.join(cur_dir, 'nyc_restaurants_by_cuisine.json'), 'r'))
    from pandas.io.json import json_normalize
    df2 = pd.DataFrame.from_dict(json_normalize(df), orient='columns')

    df3 = {}
    for i in df2.columns:
        if i == 'cuisine':
            continue
        else:
            tmp = df2[['cuisine',str(i)]].fillna(0)
            tmp.columns = ['name', 'rating']
            tmp = tmp.sort_values(by=['rating'], ascending=False)[:25]
            df3[str(i)[-5:]] = tmp
    return df3
