# Rules for House Price Prediction Project

## 1. What to Use

Use simple, reliable, and well-supported tools for this project:

- Python 3.x
- pandas for data loading and manipulation
- numpy for numerical operations
- scikit-learn for preprocessing, modeling, and evaluation
- joblib for saving and loading the trained model
- Streamlit for the web app interface
- matplotlib and seaborn for charts and visual analysis
- JSON for metadata and feature information
- pathlib for file path handling
- logging for debugging and monitoring

Use these tools to keep the project easy to understand, maintain, and deploy.

## 2. What to Avoid

Avoid unnecessary complexity or risky practices:

- Avoid heavy deep learning frameworks unless absolutely required
- Avoid using TensorFlow or PyTorch for this simple tabular regression task
- Avoid hard-coded absolute file paths
- Avoid mixing training logic and UI logic in the same file
- Avoid using `eval` or `exec` for model or data processing
- Avoid adding unused libraries to `requirements.txt`
- Avoid making manual changes to trained model files like `best_pipeline.joblib`

Keep the solution lightweight and focused on the core ML workflow.

## 3. Error Handling Rules

All code should handle errors safely and clearly:

- Validate all user inputs before prediction
- Handle missing values gracefully
- Wrap file loading, model loading, and prediction steps in `try/except`
- Show friendly error messages instead of raw stack traces to users
- Log important failures for debugging
- Fail fast if required files (such as `best_pipeline.joblib`) are missing

Example behavior:
- If the model file is missing, show a clear message
- If an input value is invalid, ask the user to correct it
- If the feature schema is changed, raise an error clearly

## 4. Boundaries and Project Structure Rules

Keep responsibilities separated:

- Training and experimentation should stay in `housing.ipynb` or training scripts
- Prediction logic should stay in `app.py`
- Model artifacts should be stored separately and reused by the app
- Feature metadata should be stored in `Charts/feature_info.json`
- Charts and metrics should stay inside the `Charts/` folder
- The app must use the same feature structure as the trained model

## 5. Coding Rules

Follow these coding rules for consistency:

- Write small, readable functions
- Use clear variable names
- Keep code modular
- Prefer simple and explainable solutions over complex ones
- Document important steps in comments where needed
- Keep the model input format consistent across training and prediction

## 6. Deployment and Maintenance Rules

- Keep dependencies listed in `requirements.txt`
- Ensure the trained model exists before running the app
- Test the app with sample inputs before deployment
- Make sure the app works with the same feature names used during training
- Prefer stable versions of libraries to avoid compatibility issues