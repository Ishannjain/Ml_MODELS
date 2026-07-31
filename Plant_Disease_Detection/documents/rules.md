# Project Rules

## Coding Rules

- Follow PEP 8 coding standards.
- Use meaningful variable names.
- Write modular functions.
- Add comments for each major block.
- Keep notebook cells organized.

---

## Dataset Rules

- Do not modify original dataset.
- Use only RGB images.
- Resize all images to 224 × 224.
- Normalize pixel values before training.

---

## Model Rules

- Use MobileNetV2 as the base model.
- Apply Transfer Learning.
- Save the best model only.
- Monitor validation accuracy.

---

## Training Rules

- Use EarlyStopping.
- Save the best weights.
- Use ModelCheckpoint.
- Prevent overfitting using Dropout.

---

## Deployment Rules

- Load the saved model.
- Accept image uploads only.
- Display prediction confidence.
- Handle invalid files gracefully.

---

## Documentation Rules

Maintain:

- README.md
- architecture.md
- PRD.md
- phases.md
- rules.md

Update documentation whenever project changes occur.

---

## GitHub Rules

- Commit after each completed phase.
- Use descriptive commit messages.
- Ignore virtual environments.
- Push code regularly.

---

## Best Practices

- Keep code readable.
- Reuse functions where possible.
- Validate user inputs.
- Save trained models in the model directory.
- Store generated figures in reports/figures.