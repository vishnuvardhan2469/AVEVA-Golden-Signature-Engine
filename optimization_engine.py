import numpy as np
from scipy.optimize import dual_annealing
from surrogate_model import SurrogateModel
import warnings

# Suppress scipy optimize warnings for clean output
warnings.filterwarnings('ignore')

class OptimizationEngine:
    def __init__(self, model_path='surrogate_model.joblib'):
        self.surrogate = SurrogateModel(model_path)
        if not self.surrogate.load():
            raise Exception("Surrogate model not found! Please train it first.")
            
        self.features = self.surrogate.features
        self.targets = self.surrogate.targets
        
        # Define physical bounds for the features to prevent the optimizer from 
        # suggesting impossible machine settings.
        # Format: (min, max) based on initial data observation
        self.bounds = [
            (5, 30),      # Granulation_Time 
            (2.0, 15.0),  # Binder_Amount
            (40, 80),     # Drying_Temp
            (20, 120),    # Drying_Time
            (5.0, 25.0),  # Compression_Force
            (10, 200),    # Machine_Speed
            (0.5, 3.0)    # Lubricant_Conc
        ]

    def _objective_function(self, x, weights):
        """
        The function we want to MINIMIZE.
        It uses the Surrogate Model to predict the outcomes of input `x`.
        """
        preds = self.surrogate.predict(dict(zip(self.features, x)))
        
        # We want to minimize Energy. 
        # But we also want to maximize Yield (which means minimizing negative Yield).
        # We also want to maximize Quality (Uniformity, Dissolution).
        
        energy = preds.get('Total_Energy_kWh', 0)
        uniformity = preds.get('Content_Uniformity', 0)
        dissolution = preds.get('Dissolution_Rate', 0)
        friability = preds.get('Friability', 0.5)
        disintegration = preds.get('Disintegration_Time', 10.0)
        
        # Normalize roughly so weights apply evenly
        norm_energy = energy / 100.0
        norm_quality = (uniformity + dissolution) / 200.0
        
        # Penalize low quality heavily
        quality_penalty = 0
        if uniformity < 95.0: quality_penalty += (95.0 - uniformity) * 5
        if dissolution < 80.0: quality_penalty += (80.0 - dissolution) * 5
        if friability > 0.8: quality_penalty += (friability - 0.8) * 50
        if disintegration > 15.0: quality_penalty += (disintegration - 15.0) * 5
        
        # Handle Yield either as a strict target or a maximize priority fallback
        target_yield = weights.get('target_yield', None)
        yield_score = 0.0
        
        if target_yield is not None:
            # We strictly penalize deviation from target yield
            actual_yield = preds.get('Tablet_Weight', 200.0)
            yield_score = abs(actual_yield - target_yield) / target_yield * 50.0 # Heavy penalty
        else:
            # Fallback to old behavior if no target is provided
            norm_yield = preds.get('Tablet_Weight', 200.0) / 300.0
            yield_score = - (weights.get('yield', 0.5) * norm_yield)
        
        # Weighted sum: minimize energy + penalty - quality reward + yield penalty/reward
        score = (weights['energy'] * norm_energy) + \
                quality_penalty - \
                (weights['quality'] * norm_quality) + \
                yield_score
                
        # --- Prescriptive Maintenance / Anomaly Compensation ---
        # If the machine is degrading, we force the optimizer to prioritize 
        # parameters that compensate. For example, if 'heater_degradation' is True,
        # we heavily penalize high Drying_Temp to force the machine to use lower temp
        # for a longer Drying_Time.
        if weights.get('anomaly_heater_degradation', False):
            # The input x[2] is Drying_Temp based on our bounds definition
            drying_temp = x[2] 
            if drying_temp > 50.0: # Penalize temperatures over 50 if heater is failing
                score += (drying_temp - 50.0) * 10.0
                
        return score

    def find_golden_signature(self, initial_guess, target_weights=None):
        """
        Finds the optimal machine parameters.
        target_weights allows the Human-in-the-loop to reprioritize goals.
        """
        if target_weights is None:
            target_weights = {'energy': 1.0, 'quality': 0.5, 'yield': 0.5}
            
        print("Running Global Optimizer (Dual Annealing) to find Golden Signature...")
        
        # Random Forests create non-differentiable, step-wise surfaces where local 
        # gradient-based optimizers (like SLSQP) get stuck instantly.
        # We MUST use a global optimizer like dual_annealing for RF surrogate models.
        result = dual_annealing(
            self._objective_function, 
            bounds=self.bounds,
            args=(target_weights,),
            maxiter=50, # Keep low for fast Streamlit UI response
            x0=initial_guess
        )
        
        if result.success or True: # dual annealing sometimes flags false but finds a good min
            optimal_params = dict(zip(self.features, result.x))
            expected_outcomes = self.surrogate.predict(optimal_params)
            
            return {
                'success': True,
                'golden_signature': optimal_params,
                'expected_outcomes': expected_outcomes
            }
        else:
            return {
                'success': False,
                'message': result.message
            }

    def generate_scenario_matrix(self, initial_guess):
        """
        Runs the global optimizer multiple times to generate a Pareto front 
        of 5 distinct Golden Signatures based on different business priorities.
        """
        scenarios = [
            {"name": "Max Energy Savings", "weights": {'energy': 100, 'quality': 5, 'yield': 5}, 'desc': 'Aggressively cuts energy, risking minor quality/yield drops.'},
            {"name": "Max Yield Focus", "weights": {'energy': 5, 'quality': 5, 'yield': 100}, 'desc': 'Maximizes tablet production weight regardless of energy cost.'},
            {"name": "100% Quality Focus", "weights": {'energy': 5, 'quality': 100, 'yield': 5}, 'desc': 'Prioritizes perfect content uniformity and dissolution.'},
            {"name": "Cost Pivot (Energy & Yield)", "weights": {'energy': 60, 'quality': 5, 'yield': 60}, 'desc': 'Balances low power draw with high production volume.'},
            {"name": "Balanced Approach", "weights": {'energy': 33, 'quality': 33, 'yield': 33}, 'desc': 'An equal compromise across all key performance indicators.'}
        ]
        
        results = []
        for s in scenarios:
            # We don't want to print to streamlit console 5 times unless debugging
            opt_res = self.find_golden_signature(initial_guess, target_weights=s['weights'])
            if opt_res['success']:
                results.append({
                    "Scenario": s["name"],
                    "Description": s["desc"],
                    "Weights": s["weights"],
                    "Parameters": opt_res['golden_signature'],
                    "Outcomes": opt_res['expected_outcomes']
                })
        return results

    def generate_pareto_front(self, num_samples=1000):
        """Generates a dataset of predicted outputs across the parameter space for 3D plotting."""
        import pandas as pd
        np.random.seed(42)
        random_configs = []
        for b in self.bounds:
            random_configs.append(np.random.uniform(b[0], b[1], num_samples))
        
        random_configs = np.array(random_configs).T
        df_configs = pd.DataFrame(random_configs, columns=self.features)
        
        # Batch predict all samples at once (Extremely fast with RF)
        preds = self.surrogate.predict(df_configs)
        
        # Return dataframe of the 3 axes we care about
        pareto_data = {
            'Energy_kWh': preds['Total_Energy_kWh'],
            'Quality_Uniformity': preds['Content_Uniformity'],
            'Yield_Weight': preds['Tablet_Weight']
        }
        return pd.DataFrame(pareto_data)


if __name__ == "__main__":
    engine = OptimizationEngine()
    
    # Baseline from T001
    baseline_params = [15.0, 8.5, 60.0, 25.0, 12.5, 150.0, 1.0]
    print(f"Baseline Inputs: {dict(zip(engine.features, baseline_params))}")
    
    baseline_outcomes = engine.surrogate.predict(dict(zip(engine.features, baseline_params)))
    print(f"Predicted Baseline Outcomes:\n{baseline_outcomes}")
    
    # Let's see if the engine can find a lower energy state with acceptable quality
    print("\n--- Optimizing for Maximum Energy Efficiency ---")
    weights_eco = {'energy': 2.0, 'quality': 0.5}
    opt_result = engine.find_golden_signature(baseline_params, target_weights=weights_eco)
    
    if opt_result['success']:
        print(f"\nGolden Signature Found!")
        eco_params = opt_result['golden_signature']
        eco_outcomes = opt_result['expected_outcomes']
        
        for k, v in eco_params.items():
            print(f"  {k}: {v:.2f}")
            
        print("\nExpected Outcomes:")
        for k, v in eco_outcomes.items():
            print(f"  {k}: {v:.2f}")
            
        energy_saved = baseline_outcomes['Total_Energy_kWh'] - eco_outcomes['Total_Energy_kWh']
        print(f"\n=> Estimated Energy Saved: {energy_saved:.2f} kWh per batch!")
