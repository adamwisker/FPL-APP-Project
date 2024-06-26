from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV, KFold
from sklearn.metrics import make_scorer, r2_score

def train_model(features, target):
    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [None, 10, 20, 30],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }
    
    rf = RandomForestRegressor(random_state=42)
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    scorer = make_scorer(r2_score, greater_is_better=True)
    
    grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=kf, n_jobs=-1, verbose=2, scoring=scorer)
    grid_search.fit(features, target)
    
    best_model = grid_search.best_estimator_
    return best_model, features.columns.tolist()
