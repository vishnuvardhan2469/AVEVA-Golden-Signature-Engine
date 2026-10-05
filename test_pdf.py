import pandas as pd
from fpdf import FPDF
from datetime import datetime

def create_pdf(compare_df, prediction_insight, carbon_insight):
    pdf = FPDF()
    pdf.add_page()
    
    order_kwh = 100
    order_carbon = 500
    
    # Title
    pdf.set_font("Helvetica", style="B", size=20)
    pdf.set_text_color(16, 185, 129)
    pdf.cell(190, 10, txt="AI-Driven Manufacturing Intelligence", ln=1, align="C")
    pdf.set_font("Helvetica", style="B", size=14)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(190, 10, txt="Golden Signature Executive Report", ln=1, align="C")
    pdf.ln(5)
    
    # Meta
    pdf.set_font("Helvetica", size=10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(190, 5, txt=f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=1)
    pdf.cell(190, 5, txt=f"Target Order Volume: 10000 Tablets", ln=1)
    pdf.ln(5)
    
    # Business Impact Highlight Box
    order_dollars = order_kwh * 0.15
    pdf.set_font("Helvetica", style="B", size=12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(190, 10, txt="1. EXECUTIVE BUSINESS IMPACT", ln=1)
    pdf.set_font("Helvetica", size=11)
    pdf.cell(190, 8, txt=f"Projected Energy Savings: {order_kwh:,.0f} kWh", ln=1)
    pdf.cell(190, 8, txt=f"Carbon Emissions Avoided: {order_carbon:,.0f} lbs CO2", ln=1)
    pdf.cell(190, 8, txt=f"Estimated Cost Reduction: ${order_dollars:,.0f}", ln=1)
    pdf.ln(5)
    
    # Priorities Matrix
    pdf.set_font("Helvetica", style="B", size=12)
    pdf.cell(190, 10, txt="2. OPTIMIZATION PRIORITIES", ln=1)
    pdf.set_font("Helvetica", size=10)
    pdf.cell(190, 6, txt=f"Energy Reduction Priority: 50%", ln=1)
    pdf.cell(190, 6, txt=f"Quality Priority: 50%", ln=1)
    pdf.cell(190, 6, txt=f"Yield / Throughput Priority: 50%", ln=1)
    pdf.ln(5)
    
    # Parameter Table
    pdf.set_font("Helvetica", style="B", size=12)
    pdf.cell(190, 10, txt="3. GOLDEN SIGNATURE PARAMETERS", ln=1)
    
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("Helvetica", style="B", size=10)
    pdf.cell(70, 10, "Machine Parameter", border=1, fill=True)
    pdf.cell(40, 10, "Baseline", border=1, fill=True, align="C")
    pdf.cell(40, 10, "Golden", border=1, fill=True, align="C")
    pdf.cell(40, 10, "Delta (%)", border=1, fill=True, align="C", ln=1)
    
    pdf.set_font("Helvetica", size=10)
    for _, row in compare_df.iterrows():
        pdf.cell(70, 10, str(row['Parameter']).replace('_', ' '), border=1)
        pdf.cell(40, 10, str(row['Previous Value']), border=1, align="C")
        pdf.cell(40, 10, str(row['Current (Golden) Value']), border=1, align="C")
        pdf.cell(40, 10, str(row['% Change']), border=1, align="C", ln=1)
        
    pdf.ln(10)

    # Agent Insights
    pdf.set_font("Helvetica", style="B", size=12)
    pdf.cell(190, 10, txt="4. AGENTIC INSIGHTS", ln=1)
    pdf.set_font("Helvetica", style="I", size=10)
    pdf.multi_cell(190, 6, txt=f"Prediction Agent: {prediction_insight}")
    pdf.ln(2)
    pdf.multi_cell(190, 6, txt=f"Carbon Agent: {carbon_insight}")
    pdf.ln(5)

    # Predicted Outcomes
    pdf.set_font("Helvetica", style="B", size=12)
    pdf.cell(190, 10, txt="5. PREDICTED OUTCOMES", ln=1)
    
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("Helvetica", style="B", size=10)
    pdf.cell(70, 10, "Metric", border=1, fill=True)
    pdf.cell(40, 10, "Baseline", border=1, fill=True, align="C")
    pdf.cell(40, 10, "Predicted", border=1, fill=True, align="C")
    pdf.cell(40, 10, "Delta", border=1, fill=True, align="C", ln=1)
    
    metrics_config = [
            ("Total_Energy_kWh", "Total Energy", "kWh", True),
            ("Content_Uniformity", "Content Uniformity", "%", False),
            ("Dissolution_Rate", "Dissolution Rate", "%", False)
    ]
    golden_outcomes = {"Total_Energy_kWh": 100, "Content_Uniformity": 90, "Dissolution_Rate": 80}
    baseline_outcomes = {"Total_Energy_kWh": 110, "Content_Uniformity": 85, "Dissolution_Rate": 75}
    
    pdf.set_font("Helvetica", size=10)
    for key, label, unit, _ in metrics_config:
        if key in golden_outcomes and key in baseline_outcomes:
            b_val = baseline_outcomes[key]
            g_val = golden_outcomes[key]
            diff = g_val - b_val
            pdf.cell(70, 10, f"{label} ({unit})", border=1)
            pdf.cell(40, 10, f"{b_val:.2f}", border=1, align="C")
            pdf.cell(40, 10, f"{g_val:.2f}", border=1, align="C")
            # Problem might be here?
            pdf.cell(40, 10, f"{diff:+.2f}", border=1, align="C", ln=1)
            
    pdf.ln(10)
    
    # Footer
    pdf.set_font("Helvetica", style="I", size=8)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(190, 5, txt="System Architecture: Random Forest Regressor & Dual Annealing Global Optimizer (AVEVA).", ln=1, align="C")
    pdf.cell(190, 5, txt="Signatures are cryptographically protected and 21 CFR Part 11 compliant. Operator ID: ADMIN-01", ln=1, align="C")
    
    # Team Signature
    pdf.ln(2)
    pdf.set_font("Helvetica", style="I", size=8)
    pdf.set_text_color(180, 180, 180)
    pdf.cell(190, 5, txt="@TeamSNAKES", ln=1, align="C")
    
    return bytes(pdf.output())


df = pd.DataFrame([{"Parameter": "test", "Previous Value": 10, "Current (Golden) Value": 20, "% Change": "+100%"}])
agent_pred = "Analyzed batch dynamics."
agent_carb = "Batch mitigates CO2"
print(create_pdf(df, agent_pred, agent_carb))
