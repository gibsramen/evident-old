import importlib

from qiime2.plugin import (Plugin, MetadataColumn, Categorical, Int, Float,
                           List, Range)
from q2_types.sample_data import SampleData, AlphaDiversity
from q2_types.distance_matrix import DistanceMatrix

from evident import __version__
from ._wrappers import (alpha_power_analysis, beta_power_analysis)
from ._format import PowerAnalysisResultsDirectoryFormat as PARsDirFmt
from ._type import PowerAnalysisResults


Probability = Float % Range(0, 1, inclusive_end=False)

param_descs = {
    "sample_metadata": "Categorical sample metadata column.",
    "alpha": "Significance level",
    "power": (
        "Probability of rejecting the null hypothesis given that the "
        "alternative is true."
    ),
    "total_observations": (
        "Total number of observations to consider. Groups are assumed to "
        "be all the same size."
    )
}


plugin = Plugin(
    name="evident",
    version=__version__,
    website="https://github.com/gibsramen/evident",
    short_description="Plugin for diversity effect size calculations",
    description=(
        "Perform power analysis on microbiome diversity data. Supports "
        "calculation of effect size given metadata covariates and supporting "
        "visualizations."
    ),
    package="evident"
)


plugin.methods.register_function(
    function=alpha_power_analysis,
    inputs={
        "alpha_diversity": SampleData[AlphaDiversity],
    },
    input_descriptions={"alpha_diversity": "Alpha diversity vector"},
    parameters={
        "sample_metadata": MetadataColumn[Categorical],
        "alpha": List[Probability],
        "power": List[Probability],
        "total_observations": List[Int]
    },
    parameter_descriptions=param_descs,
    outputs=[("power_analysis_results", PowerAnalysisResults)],
    name="Alpha diversity power analysis.",
    description=(
        "Use sample alpha diversity data to perform power calculations "
        "for desired significance level, power, or sample size."
    )
)

plugin.methods.register_function(
    function=beta_power_analysis,
    inputs={
        "beta_diversity": DistanceMatrix,
    },
    input_descriptions={"beta_diversity": "Beta diversity distance matrix"},
    parameters={
        "sample_metadata": MetadataColumn[Categorical],
        "alpha": List[Probability],
        "power": List[Probability],
        "total_observations": List[Int]
    },
    parameter_descriptions=param_descs,
    outputs=[("power_analysis_results", PowerAnalysisResults)],
    name="Beta diversity power analysis.",
    description=(
        "Use sample beta diversity data to perform power calculations "
        "for desired significance level, power, or sample size."
    )
)

plugin.register_semantic_types(PowerAnalysisResults)
plugin.register_semantic_type_to_format(
    PowerAnalysisResults,
    artifact_format=PARsDirFmt
)
plugin.register_formats(PARsDirFmt)

importlib.import_module("evident.q2._transformer")
