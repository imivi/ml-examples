1. Load Data
2. Visualize data (EDA)
3. Clean data: remove columns and/or rows
4. X/y Split
5. train_test_split. (class only: if dataset is unbalanced, use stratify)
6. Fill/Encode/Scale Data: apply this only to the training set, then use those same parameters to transform the test set
7. Check Correlation Matrix on the scaled/encoded training data
8. Pick Model & Check Training Curve: Use the default settings on your training data (via Cross-Validation) to check for overfitting
9. Grid Search: find best hyperparameters using the training set (use cross validation or validation set)
10. Train Final Model: Retrain the model on the entire training set using the best parameters found.
11. View Results: use the test set to generate your Confusion Matrix, precision/recall/F1-score (class only), or R2, mse, mae (reg only)