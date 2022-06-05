from .AbsTask import AbsTask
import datasets
import numpy as np
import logging
from collections import defaultdict
from ..evaluation.evaluators import PairClassificationEvaluator


class AbsTaskPairClassification(AbsTask):
    """
    Abstract class for PairClassificationTasks
    The similarity is computed between pairs and the results are ranked. Average precision
    is computed to measure how well the methods can be used for pairwise pair classification.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def evaluate(self, model, split="test"):
        if not self.data_loaded:
            self.load_data()

        data_split = self.dataset[split][0]

        logging.getLogger("sentence_transformers.evaluation.PairClassificationEvaluator").setLevel(logging.WARN)
        evaluator = PairClassificationEvaluator(data_split["sent1"], data_split["sent2"], data_split["labels"])
        scores = evaluator.compute_metrics(model)

        # Compute max
        max_scores = defaultdict(list)
        for sim_fct in scores:
            for metric in ["accuracy", "f1", "ap"]:
                max_scores[metric].append(scores[sim_fct][metric])

        for metric in max_scores:
            max_scores[metric] = max(max_scores[metric])

        scores["max"] = dict(max_scores)

        return scores
