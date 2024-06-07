from typing import Final

PROMPT_NAME: Final[str] = "🐍 How would you like to name the estimator?"
PROMPT_ESTIMATOR: Final[str] = "🎯 Which kind of estimator is it?"
PROMPT_REQUIRED: Final[str] = "📜 Please list the required parameters (comma-separated)"
PROMPT_OPTIONAL: Final[str] = "📑 Please list the optional parameters (comma-separated)"
PROMPT_SAMPLE_WEIGHT: Final[str] = "📶 Does the `.fit()` method support `sample_weight`?"
PROMPT_LINEAR: Final[str] = "📏 Is the estimator linear?"
PROMPT_PREDICT_PROBA: Final[str] = "🎲 Should the estimator implement a `predict_proba` method?"
PROMPT_DECISION_FUNCTION: Final[str] = "❓ Should the estimator implement a `decision_function` method?"
PROMPT_TAGS: Final[str] = (
    "🧪 We are almost there... Is there any tag you want to add? (comma-separated)\n"
    "To know more about tags, check the documentation at:\n"
    "https://scikit-learn.org/dev/developers/develop.html#estimator-tags"
)
PROMPT_OUTPUT: Final[str] = "📂 Where would you like to save the class?"
