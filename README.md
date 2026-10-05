# AVEVA Golden Signature Engine 🏭⚡

An AI-driven digital twin and optimization engine that generates "Golden Signatures" for manufacturing parameter generation. It balances energy reduction, strict quality control, and production yield dynamically in real-time.

## 🎯 Project Overview
This project provides an AI-driven framework that dynamically optimizes energy consumption and carbon emissions at the batch level while maintaining production quality and yield. By using predictive surrogate modeling and global optimization algorithms, it simulates physical operations to prescribe actionable parameter adjustments.

## 🎥 Live Demonstration
Watch the system in action, dynamically balancing energy and quality parameters through our interactive agentic workflow:

[![AVEVA Golden Signature Engine - Live Demonstration](https://img.youtube.com/vi/NDFBfur7fH4/0.jpg)](https://youtu.be/NDFBfur7fH4)

*(Click the image above to watch the full live demonstration on YouTube!)*

## 🧠 System Architecture
The solution consists of four core micro-components designed to solve non-linear manufacturing problems:

1. **`data_pipeline.py`**: Aggregates time-series batch data and merges configuration parameters to provide a unified telemetry data source.
2. **`surrogate_model.py`**: A Random Forest machine learning model trained to predict Yield, Quality, and Energy metrics based on configuration inputs. Uses an intelligent synthetic data augmentation engine to simulate wide parameter search spaces securely without real-world risk.
3. **`optimization_engine.py`**: Uses `SciPy` (`dual_annealing`) for global optimization to discover the **Golden Signature**—a Pareto-optimal machine configuration that minimizes energy use, ensures high yield, and heavily penalizes quality degradation.
4. **`app.py`**: A **Streamlit** Web Application providing real-time "Human-in-the-loop" decision support. It features interactive topography, explainable AI (SHAP) insights, and agentic workflows for plant approval.

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Activated Virtual Environment

### Installation
1. Apply a virtual environment and activate it:
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\Activate.ps1
   # macOS/Linux
   source venv/bin/activate
   ```
2. Install the necessary dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Execution
1. **Train the Surrogate Model** (Generates the `.joblib` model artifact):
   ```bash
   python surrogate_model.py
   ```
2. **Run the Application**:
   ```bash
   streamlit run app.py
   ```
3. A browser window will automatically launch the **Interactive Optimization Dashboard** at `http://localhost:8501`.

## 🌟 Core Capabilities

### 1. 🎛️ Global Optimization Hub
At the heart of the AVEVA Golden Signature Engine is the Global Optimization Hub. This interactive control unit allows plant managers and operators to set dynamic, real-time priorities across competing objectives: **Energy Reduction**, **Strict Quality Control**, and **Throughput/Yield**.
- **How it works:** Depending on the specific business needs for a production run (e.g., meeting a sustainability target vs. hitting a tight deadline), operators flexibly adjust priority weights. The system feeds these macro-parameters into a powerful global multivariate optimization algorithm (`SciPy`'s `dual_annealing`).
- **The Value:** Instead of relying on static, outdated machine configurations or operator intuition, the factory dynamically adapts its machinery parameters to match precise executive strategies instantly.

### 2. 📊 Predictive Impact Analysis & Carbon Tracking
Before a single physical machine parameter is altered, the engine simulates the entire run using its AI digital twin. It presents a comprehensive, real-time comparison between the historical baseline signature and the newly proposed optimal "Golden Signature."
- **How it works:** The system actively calculates the comparative percent changes across all non-linear outcome variables (like Dissolution Rate, Hardness, and Granulation Time). Furthermore, it aggressively computes the **Total Energy Saved (kWh)** and **Carbon Emissions Avoided (lbs CO₂)** required for the entire order volume.
- **The Value:** Provides executive-level financial and environmental metrics up-front, guaranteeing that sustainability KPIs and strict cost-reduction goals will be met reliably and safely before actual production begins.

### 3. 🧠 Explainable AI (XAI) & Dynamic Model Trust
The system completely abandons the "black-box" AI paradigm prevalent in most machine learning operations. It leverages cutting-edge **SHAP (SHapley Additive exPlanations)** analysis to explicitly reveal how the AI derived its optimal signature.
- **How it works:** A bespoke XAI dashboard dynamically charts the relative feature importance for *each specific batch calculation*. If the AI predicts that lowering the oven temperature and exponentially increasing machine speed is the ideal path, the XAI layer demonstrates exactly mathematically *why* those specific dials are the primary drivers. 
- **The Value:** Builds absolute confidence and trust for human operators, providing a "plain English" translation of complex, multi-dimensional machine learning logic so engineers understand the "why" behind the AI's recommendations.

### 4. 🌌 3D Pareto Frontier Topography Mapping
The platform features an advanced, interactive 3D visualizer that physically maps the theoretical limitations of the manufacturing process architecture.
- **How it works:** By executing thousands of simulated batch trajectories through the Random Forest surrogate model, the platform charts a multidimensional "cloud" of potential outcomes in real-time. It then isolates and highlights the Golden Signature—the mathematically proven optimal point residing perfectly balanced on the Pareto-efficient frontier.
- **The Value:** Transforms invisible mathematical arrays into a tangible, topographical map. This allows engineers to visually verify that they are pushing the absolute boundaries of plant physics to maximize efficiency without stepping into product failure zones.

### 5. 🤖 Agentic Workflows & Compliance Reporting
The system integrates an automated, intelligent background "Agent Swarm" that actively monitors the generated parameters to ensure regulatory compliance and total operational safety.
- **How it works:** Localized intelligent agents continually scan thousands of parameter combinations, running autonomous checks against rigid emissions limits (e.g., ensuring total order volume stays under 50k lbs of CO₂ emissions) and enforcing 21 CFR Part 11 auditing standards. Upon operator verification, a dedicated agent seamlessly compiles all predictions, deviations, and comparative metrics into a cryptographically secured **PDF Executive Report**.
- **The Value:** Automates the severe bureaucratic friction of plant approvals, turning weeks of data amalgamation, analysis, and manual reporting into a verified, single-click deployment pathway.
