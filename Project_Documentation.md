# AVEVA Golden Signature Engine - Project Documentation

## 1. Problem Statement
Modern manufacturing processes face a continuous challenge: balancing the conflicting objectives of minimizing energy consumption and carbon emissions, while simultaneously ensuring strict quality control and maximizing production yield. Traditional parameter tuning is often reactive, manual (relying on operator intuition), and lacks the capability to explore high-dimensional configuration spaces dynamically without risking physical production batches. There is a critical need for an intelligent, predictive system that can proactively optimize machine configurations in real-time to achieve sustainability targets without compromising production KPIs.

## 2. How We Solve It
We introduce the **AVEVA Golden Signature Engine**, an AI-driven digital twin and optimization engine framework. 
The solution operates by decoupling the physical risk from parameter exploration. It uses a **predictive surrogate model**—a machine learning algorithm trained on historical and augmented batch data—to simulate the physical operations of the plant. 
Once the simulated environment is established, a **global optimization algorithm** explores this multidimensional space to discover the "Golden Signature." This signature represents the Pareto-optimal set of machine parameters that minimizes energy use, maximizes yield, and heavily penalizes quality degradation, perfectly tailored to the real-time operational priorities set by the plant managers.

## 3. Tech Stack Used
* **Core Language:** Python 3.9+
* **Machine Learning:** Scikit-Learn (Random Forest Regressor)
* **Optimization:** SciPy (`dual_annealing` for global multivariate optimization)
* **Explainable AI (XAI):** SHAP (SHapley Additive exPlanations)
* **Web Application/UI:** Streamlit
* **Data Processing:** Pandas, NumPy
* **Visualization:** Plotly (for interactive 3D Pareto Frontier mapping), Matplotlib
* **Reporting:** FPDF (for agentic PDF report generation)

## 4. Key Features
* **Global Optimization Hub:** An interactive control center where users can set dynamic weights and priorities for Energy, Quality, and Yield depending on the current production run's requirements.
* **Predictive Impact Analysis:** Real-time projection of the optimized outcomes compared against baseline performance, including the calculation of total order carbon avoidance.
* **Explainable AI (XAI) Integration:** Dynamic visualization of SHAP values to explain the relative importance of each parameter in the AI's decision-making process, fostering human trust.
* **3D Pareto Frontier Mapping:** A visual representation charting the "Golden Signature" inside a multi-dimensional topography cloud of simulated scenarios, showing how the optimal point balances the trade-offs.
* **Agentic Workflows:** Automated compliance checking, tracking of predictions, and the ability to generate and export PDF executive reports to streamline plant approval processes.

## 5. How It Works
The system follows a sequential, four-pillar architecture to solve the non-linear manufacturing problem:

1. **Data Ingestion (`data_pipeline.py`):** Aggregates time-series batch data and merges it with process configuration parameters to provide a unified telemetry data source.
2. **Surrogate Modeling (`surrogate_model.py`):** A Random Forest model is trained to learn the complex relationships between configuration inputs (e.g., temperatures, pressures) and the resulting Yield, Quality, and Energy metrics. It employs intelligent synthetic data augmentation to securely simulate wide parameter search spaces.
3. **Optimization Engine (`optimization_engine.py`):** Driven by the priorities set by the user, this module uses SciPy's `dual_annealing` function to navigate the surrogate model's predictions. It mathematically discovers the best configuration (Golden Signature) that satisfies the specific weighted constraints of the current batch.
4. **Human-in-the-Loop Web Application (`app.py`):** The Streamlit frontend acts as the interface. It gathers user priorities, triggers the optimization engine in real-time, and presents the recommended actions, XAI insights, and predictive impacts in an intuitive, interactive dashboard for final executive approval.
