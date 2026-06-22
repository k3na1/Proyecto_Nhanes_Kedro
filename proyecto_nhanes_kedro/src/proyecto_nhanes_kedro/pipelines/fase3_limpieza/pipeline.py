from kedro.pipeline import Pipeline, node
from .nodes import recode_nhanes_special_values, drop_high_null_columns, drop_high_null_rows, drop_low_variance_columns

def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline([
        node(
            func=recode_nhanes_special_values,
            inputs="demolab_master",
            outputs="demolab_recoded",
            name="recode_demolab"
        ),
        node(
            func=drop_high_null_columns,
            inputs="demolab_recoded",
            outputs="demolab_cols_cleaned",
            name="drop_null_cols_demolab"
        ),
        node(
            func=drop_high_null_rows,
            inputs="demolab_cols_cleaned",
            outputs="demolab_rows_cleaned",
            name="drop_null_rows_demolab"
        ),
        node(
            func=drop_low_variance_columns,
            inputs="demolab_rows_cleaned",
            outputs="demolab_clean",
            name="drop_low_var_demolab"
        )
    ])
