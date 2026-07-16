# Development Rules

## Coding Standards

- Follow PEP8 formatting
- Write reusable functions
- Avoid duplicate code
- Use modular programming
- Add comments for clarity
- Use meaningful variable names

## Folder Rules

- Store raw and cleaned data inside `dataset/`
- Save models inside `model/`
- Place source code inside `src/`
- Keep notebooks inside `notebook/`
- Save reports inside `reports/`
- Save charts and visualizations inside `charts/`

## Git Rules

- Commit changes after completing each phase
- Use clear commit message format:
  - `Phase-1 Environment Setup`
  - `Phase-2 EDA`
  - `Phase-3 NLP`
  - `Phase-4 Training`
  - `Phase-5 Evaluation`

## Model Artifact Rules

- Always save trained artifacts:
  - `spam_model.pkl`
  - `tfidf.pkl`
  - `label_encoder.pkl`
- Do not overwrite artifacts without a backup

## Documentation Rules

- Maintain the following documentation files:
  - `readme.md`
  - `documents/phases.md`
  - `documents/architecture.md`
  - `documents/rules.md`
  - `requirements.txt`

## Naming Conventions

- Use `snake_case` for functions and variables
- Examples:
  - `train_model()`
  - `clean_text()`
  - `predict_spam()`

## Notebook Rules

- Keep one main notebook for EDA and experiments
- Use clear section headings
- Save plotted charts to `charts/`

## Streamlit Rules

- Use a sidebar for user input
- Set page configuration
- Handle exceptions gracefully
- Display prediction results clearly
- Show model confidence when available

## Deployment Rules

- Push the project to GitHub
- Deploy using Streamlit Cloud or a similar service
- Keep the README updated with deployment instructions
- Add screenshots or demo links when available

## Project Goals

- Production ready
- Deployment ready
- Portfolio ready
- Interview ready