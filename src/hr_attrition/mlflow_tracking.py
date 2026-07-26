def configure_mlflow(
    tracking_uri: str,
    experiment_name: str,
) -> None:
    mlflow.set_tracking_uri(tracking_uri)
    experiment = mlflow.set_experiment(experiment_name)

    print("MLflow tracking URI:", mlflow.get_tracking_uri())
    print("MLflow experiment:", experiment.name)
    print("MLflow experiment ID:", experiment.experiment_id)