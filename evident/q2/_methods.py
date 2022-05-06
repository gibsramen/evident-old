from typing import List

import pandas as pd
from qiime2 import CategoricalMetadataColumn, Metadata
from skbio import DistanceMatrix

from evident import UnivariateDataHandler, BivariateDataHandler
from evident.diversity_handler import (
    RepeatedMeasuresUnivariateDataHandler as RDH
)
from evident.effect_size import (effect_size_by_category,
                                 pairwise_effect_size_by_category)


def alpha_power_analysis(
    alpha_diversity: pd.Series,
    sample_metadata: CategoricalMetadataColumn,
    max_levels_per_category: int = 5,
    min_count_per_level: int = 3,
    alpha: list = None,
    power: list = None,
    total_observations: list = None,
    difference: list = None,
) -> pd.DataFrame:
    res = _power_analysis(alpha_diversity, sample_metadata,
                          UnivariateDataHandler,
                          max_levels_per_category, min_count_per_level,
                          alpha=alpha, power=power,
                          total_observations=total_observations,
                          difference=difference)
    return res


def beta_power_analysis(
    beta_diversity: DistanceMatrix,
    sample_metadata: CategoricalMetadataColumn,
    max_levels_per_category: int = 5,
    min_count_per_level: int = 3,
    alpha: list = None,
    power: list = None,
    total_observations: list = None,
    difference: list = None,
) -> pd.DataFrame:
    res = _power_analysis(beta_diversity, sample_metadata,
                          BivariateDataHandler,
                          max_levels_per_category, min_count_per_level,
                          alpha=alpha, power=power,
                          total_observations=total_observations,
                          difference=difference)
    return res


def _power_analysis(data, metadata, handler, max_levels_per_category,
                    min_count_per_level, **kwargs):
    md = metadata.to_series()
    column = md.name
    dh = handler(data, md.to_frame(), max_levels_per_category,
                 min_count_per_level)
    res = dh.power_analysis(column, **kwargs)
    return res.to_dataframe()


def alpha_effect_size_by_category(
    alpha_diversity: pd.Series,
    sample_metadata: Metadata,
    columns: List[str],
    pairwise: bool = False,
    n_jobs: int = None,
    max_levels_per_category: int = 5,
    min_count_per_level: int = 3
) -> pd.DataFrame:
    res = _effect_size_by_category(alpha_diversity, sample_metadata,
                                   UnivariateDataHandler, columns, pairwise,
                                   n_jobs, max_levels_per_category,
                                   min_count_per_level)
    return res


def beta_effect_size_by_category(
    beta_diversity: DistanceMatrix,
    sample_metadata: Metadata,
    columns: List[str],
    pairwise: bool = False,
    n_jobs: int = None,
    max_levels_per_category: int = 5,
    min_count_per_level: int = 3
) -> pd.DataFrame:
    res = _effect_size_by_category(beta_diversity, sample_metadata,
                                   BivariateDataHandler, columns, pairwise,
                                   n_jobs, max_levels_per_category,
                                   min_count_per_level)
    return res


def _effect_size_by_category(data, metadata, handler, columns, pairwise,
                             n_jobs, max_levels_per_category,
                             min_count_per_level):
    dh = handler(data, metadata.to_dataframe(), max_levels_per_category,
                 min_count_per_level)
    if pairwise:
        res = pairwise_effect_size_by_category(dh, columns, n_jobs=n_jobs)
    else:
        res = effect_size_by_category(dh, columns, n_jobs=n_jobs)
    return res.to_dataframe()


def alpha_power_analysis_repeated_measures(
    alpha_diversity: pd.Series,
    sample_metadata: Metadata,
    individual_id_column: str,
    state_column: str,
    subjects: list = None,
    measurements: list = None,
    alpha: list = None,
    correlation: list = None,
    epsilon: list = None,
    max_levels_per_category: int = 5,
    min_count_per_level: int = 3,
) -> pd.DataFrame:
    dh = RDH(alpha_diversity, sample_metadata.to_dataframe(),
             individual_id_column, max_levels_per_category,
             min_count_per_level)

    results = dh.power_analysis(
        state_column,
        subjects,
        measurements,
        alpha,
        correlation,
        epsilon
    ).to_dataframe()

    return results
