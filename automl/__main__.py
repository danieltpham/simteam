from surrogate_trainer import SurrogateTrainer

trainer = SurrogateTrainer()

# Train and print 10-fold CV results
cv_df = trainer.train_with_cv()
print(cv_df)

# Fit final model and save
trainer.fit_full()
trainer.save()
