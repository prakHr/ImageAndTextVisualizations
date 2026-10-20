
import os
os.environ["OMP_NUM_THREADS"] = "1"

import traceback
import numpy as np

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression

from hyperopt import tpe
from hpsklearn import HyperoptEstimator
from hpsklearn.components import (
    ada_boost_classifier,
    extra_tree_classifier,
    extra_trees_classifier,
    decision_tree_classifier,
    gaussian_nb,
    quadratic_discriminant_analysis,
    passive_aggressive_classifier,
    sgd_classifier,
    linear_svc,
    xgboost_classification,
    linear_discriminant_analysis,
    random_forest_classifier,
    k_neighbors_classifier,
    svc,
    lightgbm_classification,
)

from lazypredict.Supervised import LazyClassifier
from vecstack import stacking


def get_awesome_accuracy(
    X,
    y,
    test_size,
    random_state,
):
    # Split the dataset.
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y,
    )

    # Evaluate initial models.
    clf = LazyClassifier(
        verbose=0,
        ignore_warnings=True,
        custom_metric=None,
    )

    models, predictions = clf.fit(
        X_train,
        X_test,
        y_train,
        y_test,
    )

    # Sort models by initial accuracy.
    models_and_scores = sorted(
        [
            (name, float(score))
            for name, score in models["Accuracy"].items()
        ],
        key=lambda item: item[1],
    )


    # Map LazyClassifier names to Hyperopt-Sklearn components.
    classifier_spaces = {
        "AdaBoostClassifier": ada_boost_classifier,
        "ExtraTreeClassifier": extra_tree_classifier,
        "GaussianNB": gaussian_nb,
        "DecisionTreeClassifier": decision_tree_classifier,
        "QuadraticDiscriminantAnalysis":
            quadratic_discriminant_analysis,
        "PassiveAggressiveClassifier":
            passive_aggressive_classifier,
        "SGDClassifier": sgd_classifier,
        "LinearSVC": linear_svc,
        "XGBClassifier": xgboost_classification,
        "LinearDiscriminantAnalysis":
            linear_discriminant_analysis,
        "RandomForestClassifier": random_forest_classifier,
        "ExtraTreesClassifier": extra_trees_classifier,
        "KNeighborsClassifier": k_neighbors_classifier,
        "SVC": svc,
        "LGBMClassifier": lightgbm_classification,
    }

    best_models_list = []
    best_model = None
    max_accuracy = -1.0

    # Optimize models below the requested accuracy threshold.
    for name, accuracy in models_and_scores:

        classifier = classifier_spaces.get(name)

        if classifier is None:
            
            continue

        try:

            estim = HyperoptEstimator(
                classifier=classifier(name),
                algo=tpe.suggest,
                max_evals=1,
                trial_timeout=120,
            )

            estim.fit(X_train, y_train)

            # Evaluate the optimized estimator.
            score = estim.score(X_test, y_test)
            # print(f"Optimized accuracy: {score:.4f}")

            # Inspect the best-model structure.
            best_model_info = estim.best_model()

            if not best_model_info:
                continue

            # Hyperopt-Sklearn commonly returns a dictionary
            # containing the fitted learner and preprocessing.

            # Keep the complete fitted pipeline when available.
            best_estimator = best_model_info.get("learner")

            if best_estimator is None:
                continue

            best_models_list.append(best_estimator)

            if score > max_accuracy:
                max_accuracy = score
                best_model = best_estimator

            

        except Exception as e:
            pass
    

    # Generate out-of-fold predictions for the meta-model.
    S_train, S_test = stacking(
        best_models_list,
        X_train,
        y_train,
        X_test,
        regression=False,
        mode="oof_pred_bag",
        needs_proba=False,
        save_dir=None,
        metric=accuracy_score,
        n_folds=4,
        stratified=True,
        shuffle=True,
        random_state=0,
        verbose=2,
    )

    # Train the second-level classifier.
    meta_model = best_model

    meta_model.fit(S_train, y_train)

    # Make final predictions.
    y_pred = meta_model.predict(S_test)
    final_accuracy = accuracy_score(y_test, y_pred)


    return {
        "best_models_at_1st_level": best_models_list,
        "best_model_at_2nd_level": meta_model,
        "final_accuracy": final_accuracy,
    }


if __name__ == "__main__":

    # Load the Iris dataset.
    iris = load_iris()
    X, y = iris.data, iris.target

    test_size = 0.2
    random_state = 42

    results = get_awesome_accuracy(
        X=X,
        y=y,
        test_size=test_size,
        random_state=random_state,
    )

    print("\nFinal results:")
    print(results)
