import optuna
from ultralytics import YOLO
from codecarbon import EmissionsTracker

# Definer objektivfunksjonen for hyperparameter-søk
def objective(trial):
    # Velg hyperparametere som Optuna skal prøve ut
    learning_rate = trial.suggest_loguniform("learning_rate", 1e-5, 1e-1)
    momentum = trial.suggest_float("momentum", 0.6, 0.98)
    weight_decay = trial.suggest_loguniform("weight_decay", 1e-5, 1e-2)

    # Last inn YOLO-modellen
    model = YOLO("yolo11n.pt")

    tracker = EmissionsTracker()
    tracker.start()
    # Tren modellen med de valgte hyperparameterne
    model.train(data="datasets/data.yaml", epochs=10, lr0=learning_rate, momentum=momentum, weight_decay=weight_decay)

    metrics = model.val()
    precision, recall, mAP, f1, ap_class = metrics.results_dict.values()

    emissions = tracker.stop()
    print("CO2 emissions:", emissions)

    # Returner beste mAP (mean Average Precision) som målfunksjon
    return 

# Opprett en Optuna-studie
study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=20)  # Kjører 20 forsøk med ulike hyperparametere

# Vis de beste hyperparameterne
print("Best hyperparameters:", study.best_params)
