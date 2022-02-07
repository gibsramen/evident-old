from abc import ABC, abstractmethod
from functools import partial
from typing import Callable, Union

import numpy as np
import pandas as pd
from skbio import DistanceMatrix
from statsmodels.stats.power import tt_ind_solve_power, FTestAnovaPower

from .exceptions import NoSamplesError


class BaseDiversityHandler(ABC):
    def __init__(self, data = None, metadata: pd.DataFrame = None):
        self.data = data
        self.metadata = metadata

    @property
    def samples(self):
        return self.metadata.index.to_list()

    @abstractmethod
    def power_analysis(
        self,
        power_function: Callable,
        effect_size: float,
        alpha: float = None,
        power: float = None
    ):
        """Perform power analysis using this dataset

        NOTE: Only really makes sense when *not* specifying effect size.
              Use diversity for effect size calculation depending on groups.
              Maybe allow specificying difference?

        Observations calculated in _incept_power_solve_function and is
            included in power_function
        """
        val_to_solve = power_function(
            effect_size=effect_size,
            power=power,
            alpha=alpha
        )
        return val_to_solve

    def _incept_power_solve_function(
        self,
        column: str,
        total_observations: int = None
    ) -> Callable:
        """Create basic function to solve for power.

        :param column: Name of column in metadata to consider
        :type column: str

        :param total_observations: Total number of observations for power
            calculation, defaults to None
        :type total_observations: int

        :returns: Stem of power function based on chosen column
        :rtype: partial function
        """
        if self.metadata[column].dtype != np.dtype("object"):
            raise ValueError("Column must be of dtype object!")

        column_choices = self.metadata[column].unique()
        num_choices = len(column_choices)

        if num_choices == 1:
            raise ValueError("Only one column value!")
        elif num_choices == 2:
            # tt_ind_solve_power uses observations per group
            if total_observations is not None:
                total_observations = total_observations / 2
            power_func = partial(
                tt_ind_solve_power
                nobs1=total_observations,
                ratio=1.0
            )
        else:
            # FTestAnovaPower uses *total* observations
            power_func = partial(
                FTestAnovaPower().solve_power,
                k_groups=num_choices,
                nobs=total_observations
            )

        return power_func

class AlphaDiversityHandler(BaseDiversityHandler):
    def __init__(
        self,
        data: pd.Series,
        metadata: pd.DataFrame
    ):
        md_samps = set(metadata.index)
        data_samps = set(data.index)
        samps_in_common = md_samps.intersection(data_samps)

        super().__init__(
            data=data.loc[samps_in_common],
            metadata=metadata.loc[samps_in_common]
        )

    def power_analysis(
        self,
        column: str,
        total_observations: int = None,
        difference: float = None
        alpha: float = None,
        power: float = None
    ):
        power_func = self._incept_power_solve_function(
            column=column,
            total_observation=total_observations
        )

        return


# class BetaDiversityHandler(BaseDiversityHandler):
#     def __init__(
#         self,
#         data: DistanceMatrix,
#         metadata: pd.DataFrame
#     ):
#         md_samps = set(metadata.index)
#         data_samps = set(data.ids)
#         samps_in_common = md_samps.intersection(data_samps)
# 
#         super().__init__(
#             data=data.filter(samps_in_common),
#             metadata=metadata.loc[samps_in_common]
#         )
