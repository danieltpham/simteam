target_cols = [
    "total_num_hired", "total_num_left", "total_num_promoted", "org_saturation_day",
    "vp_team_size_skew", "director_team_size_skew", "manager_team_size_skew",
    "mean_days_between_hires", "mean_days_between_promotions", "mean_days_between_leavings"
]

automl_settings = {
    "time_budget": 10,
    "task": "regression",
    "metric": "rmse",
    "estimator_list": ["xgboost"],
    "log_file_name": "flaml.log",
    "verbose": 2,
    "early_stop": True,
    "n_jobs": 4,  # Set to >1 if you want parallelism
}
