import streamlit as st
import pandas as pd

# ==========================================
# 1. CONFIGURATION & LANGUAGE SETUP
# ==========================================
st.set_page_config(page_title="Restaurant Financial Simulator", layout="wide")

# Language Dictionary
LANG = {
    "PT": {
        "title": "Simulador Financeiro para Restaurantes",
        "sidebar_header": "Configurações de Custos",
        "reset_btn": "Resetar Valores",
        "lang_select": "Idioma / Language",
        "dish_cost": "Custo do Prato (CMV) R$",
        "curr_price": "Preço de Venda Atual R$",
        "tax_rate": "Impostos (%)",
        "app_rate": "Taxa do App/Comissão (%)",
        "fixed_rate": "Custos Fixos/Admin (%)",
        "ads_rate": "Marketing/Ads (%)",
        "delivery_rate": "Custo de Entrega/Logística (%)",
        "profit_rate": "Margem de Lucro Desejada (%)",
        "sec1_title": "1. Análise de Precificação e Meta",
        "curr_perf": "Desempenho Atual",
        "curr_net_profit": "Lucro Líquido Atual",
        "ideal_rec": "Recomendação Ideal",
        "ideal_price": "Preço de Venda Ideal",
        "target_cmv": "CMV Alvo (no Preço Ideal)",
        "breakdown_title": "Composição do Preço Ideal (R$)",
        "col_component": "Componente",
        "col_value": "Valor (R$)",
        "comp_cmv": "Custo Mercadoria (CMV)",
        "comp_tax": "Impostos",
        "comp_app": "Comissão App",
        "comp_fixed": "Custos Fixos",
        "comp_ads": "Marketing",
        "comp_del": "Entrega",
        "comp_profit": "Lucro Líquido Desejado",
        "sec2_title": "2. Simulador de Promoções",
        "coupon_label": "Desconto do Cupom (%)",
        "promo_impact": "Impacto da Promoção",
        "price_post_coupon": "Preço Pós-Cupom",
        "new_cmv": "Novo % CMV",
        "new_net_profit": "Novo Lucro Líquido",
        "breakeven_title": "Análise de Ponto de Equilíbrio (Break-even)",
        "vol_needed": "Aumento de Vendas Necessário",
        "to_maintain": "para manter o mesmo lucro total atual",
        "risk_alert": "ALERTA DE RISCO: Prejuízo por venda!",
        "impossible": "Impossível (Prejuízo)",
        "error_margin": "A soma das taxas (sem lucro) é >= 100%. Impossível calcular lucro.",
        "error_ideal": "A soma total das taxas (com lucro) é >= 100%. Impossível fixar preço ideal."
    },
    "EN": {
        "title": "Restaurant Financial Simulator",
        "sidebar_header": "Cost Configuration",
        "reset_btn": "Reset Values",
        "lang_select": "Language / Idioma",
        "dish_cost": "Dish Cost (CMV) $",
        "curr_price": "Current Selling Price $",
        "tax_rate": "Tax Rate (%)",
        "app_rate": "App Commission (%)",
        "fixed_rate": "Fixed Costs (%)",
        "ads_rate": "Ads/Marketing (%)",
        "delivery_rate": "Delivery Cost (%)",
        "profit_rate": "Desired Net Profit Rate (%)",
        "sec1_title": "1. Pricing Analysis & Targets",
        "curr_perf": "Current Performance",
        "curr_net_profit": "Current Net Profit",
        "ideal_rec": "Ideal Recommendation",
        "ideal_price": "Ideal Selling Price",
        "target_cmv": "Target CMV (at Ideal Price)",
        "breakdown_title": "Ideal Price Breakdown ($)",
        "col_component": "Component",
        "col_value": "Value ($)",
        "comp_cmv": "Dish Cost (CMV)",
        "comp_tax": "Taxes",
        "comp_app": "App Commission",
        "comp_fixed": "Fixed Costs",
        "comp_ads": "Marketing",
        "comp_del": "Delivery",
        "comp_profit": "Desired Net Profit",
        "sec2_title": "2. Promotion Simulator",
        "coupon_label": "Coupon Discount (%)",
        "promo_impact": "Promotion Impact",
        "price_post_coupon": "Price Post-Coupon",
        "new_cmv": "New CMV %",
        "new_net_profit": "New Net Profit",
        "breakeven_title": "Break-even Analysis",
        "vol_needed": "Sales Volume Increase Needed",
        "to_maintain": "to maintain same total profit",
        "risk_alert": "RISK ALERT: Loss per sale!",
        "impossible": "Impossible (Loss)",
        "error_margin": "Sum of expense rates is >= 100%. Impossible to calculate profit.",
        "error_ideal": "Sum of all rates (w/ profit) is >= 100%. Impossible to set ideal price."
    }
}

# ==========================================
# 2. SESSION STATE & RESET
# ==========================================
DEFAULTS = {
    "dish_cost": 15.00,
    "current_price": 45.00,
    "tax_rate": 8.0,
    "app_rate": 12.0,
    "fixed_rate": 10.0,
    "ads_rate": 3.0,
    "delivery_rate": 2.0,
    "profit_rate": 20.0,
    "coupon_rate": 0.0,
    "lang_choice": "EN" # Default language set to ENGLISH
}

def init_session_state():
    for key, value in DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value

def reset_inputs():
    for key, value in DEFAULTS.items():
        if key != "lang_choice": # Keep language selection
            st.session_state[key] = value

init_session_state()

# ==========================================
# 3. SIDEBAR & INPUTS
# ==========================================
st.sidebar.title("Settings / Config")

# Language Selector
lang_options = ["PT", "EN"]
selected_lang = st.sidebar.radio(
    LANG[st.session_state["lang_choice"]]["lang_select"],
    lang_options,
    index=lang_options.index(st.session_state["lang_choice"])
)
st.session_state["lang_choice"] = selected_lang
T = LANG[st.session_state["lang_choice"]] # Current translation dict

st.sidebar.markdown("---")
st.sidebar.header(T["sidebar_header"])

if st.sidebar.button(T["reset_btn"]):
    reset_inputs()
    st.rerun()

# Financial Inputs
dish_cost = st.sidebar.number_input(T["dish_cost"], min_value=0.0, value=st.session_state["dish_cost"], step=0.50)
current_price = st.sidebar.number_input(T["curr_price"], min_value=0.0, value=st.session_state["current_price"], step=0.50)

st.sidebar.markdown("---")
# Rate Sliders
tax_rate = st.sidebar.slider(T["tax_rate"], 0.0, 100.0, st.session_state["tax_rate"]) / 100.0
app_rate = st.sidebar.slider(T["app_rate"], 0.0, 100.0, st.session_state["app_rate"]) / 100.0
fixed_rate = st.sidebar.slider(T["fixed_rate"], 0.0, 100.0, st.session_state["fixed_rate"]) / 100.0
ads_rate = st.sidebar.slider(T["ads_rate"], 0.0, 100.0, st.session_state["ads_rate"]) / 100.0
delivery_rate = st.sidebar.slider(T["delivery_rate"], 0.0, 100.0, st.session_state["delivery_rate"]) / 100.0
profit_rate = st.sidebar.slider(T["profit_rate"], 0.0, 100.0, st.session_state["profit_rate"]) / 100.0

# Update Session State with slider values
st.session_state["dish_cost"] = dish_cost
st.session_state["current_price"] = current_price

# ==========================================
# 4. CORE LOGIC CALCULATIONS
# ==========================================

total_operating_expenses = tax_rate + app_rate + fixed_rate + ads_rate + delivery_rate
total_rates_with_profit = total_operating_expenses + profit_rate

current_net_profit = (current_price * (1 - total_operating_expenses)) - dish_cost
current_cmv_percent = (dish_cost / current_price * 100) if current_price > 0 else 0

if total_rates_with_profit >= 1.0:
    ideal_price = float('inf')
    ideal_cmv_percent = 0
else:
    ideal_price = dish_cost / (1 - total_rates_with_profit)
    ideal_cmv_percent = (dish_cost / ideal_price * 100) if ideal_price > 0 else 0

# ==========================================
# 5. DASHBOARD UI - SECTION 1
# ==========================================
st.title(T["title"])

st.header(T["sec1_title"])
col1, col2 = st.columns(2)

# Current Performance
with col1:
    st.subheader(T["curr_perf"])
    st.metric(label=T["curr_price"], value=f"R$ {current_price:.2f}")
    st.metric(label="Current CMV (%)", value=f"{current_cmv_percent:.1f}%")
    
    # Styling Net Profit based on value
    profit_color = "green" if current_net_profit > 0 else "red"
    st.markdown(f"""
    <div style="padding:10px; border-radius:5px; background-color:rgba(200,200,200,0.1); border:1px solid #ddd;">
        <small>{T["curr_net_profit"]}</small><br>
        <span style="color:{profit_color}; font-size:24px; font-weight:bold;">
            R$ {current_net_profit:.2f}
        </span>
    </div>
    """, unsafe_allow_html=True)

# Ideal Recommendation
with col2:
    st.subheader(T["ideal_rec"])
    if ideal_price == float('inf'):
        st.error(T["error_ideal"])
    else:
        st.metric(label=T["ideal_price"], value=f"R$ {ideal_price:.2f}", delta=f"R$ {ideal_price - current_price:.2f}")
        st.metric(label=T["target_cmv"], value=f"{ideal_cmv_percent:.1f}%")

# Breakdown Table (Calculated on Ideal Price)
st.write(f"**{T['breakdown_title']}**")
if ideal_price != float('inf'):
    
    breakdown_data = {
        T["col_component"]: [
            T["comp_cmv"], 
            T["comp_tax"], 
            T["comp_app"], 
            T["comp_fixed"], 
            T["comp_ads"], 
            T["comp_del"], 
            T["comp_profit"]
        ],
        T["col_value"]: [
            dish_cost,
            ideal_price * tax_rate,
            ideal_price * app_rate,
            ideal_price * fixed_rate,
            ideal_price * ads_rate,
            ideal_price * delivery_rate,
            ideal_price * profit_rate
        ]
    }
    df_breakdown = pd.DataFrame(breakdown_data) # <--- FIX APPLIED HERE!
    st.dataframe(df_breakdown.style.format({T["col_value"]: "R$ {:.2f}"}), use_container_width=True, hide_index=True)

st.markdown("---")

# ==========================================
# 6. DASHBOARD UI - SECTION 2
# ==========================================
st.header(T["sec2_title"])

coupon_percent = st.slider(T["coupon_label"], 0, 100, 0)
coupon_rate = coupon_percent / 100.0

# Calculations for Promo
price_post_coupon = current_price * (1 - coupon_rate)
new_cmv_percent = (dish_cost / price_post_coupon * 100) if price_post_coupon > 0 else 0

new_net_profit = (price_post_coupon * (1 - total_operating_expenses)) - dish_cost

col_promo1, col_promo2 = st.columns(2)

with col_promo1:
    st.subheader(T["promo_impact"])
    st.metric(label=T["price_post_coupon"], value=f"R$ {price_post_coupon:.2f}")
    st.metric(label=T["new_cmv"], value=f"{new_cmv_percent:.1f}%")
    
    # Visual check for profit
    new_profit_color = "green" if new_net_profit > 0 else "red"
    st.markdown(f"""
    <div style="border-left: 5px solid {new_profit_color}; padding-left: 10px;">
        <small>{T["new_net_profit"]}</small><br>
        <span style="font-size:22px; font-weight:bold;">R$ {new_net_profit:.2f}</span>
    </div>
    """, unsafe_allow_html=True)

with col_promo2:
    st.subheader(T["breakeven_title"])
    
    if current_net_profit <= 0:
        st.warning("Current operation is already at a loss or zero profit.")
    elif new_net_profit <= 0:
        st.error(f"**{T['risk_alert']}**")
        st.metric(label=T["vol_needed"], value=T["impossible"])
    else:
        needed_increase_ratio = (current_net_profit / new_net_profit)
        needed_increase_percent = (needed_increase_ratio - 1) * 100
        
        if needed_increase_percent < 0:
            st.success("Profit margin improved.")
        else:
            st.metric(label=T["vol_needed"], value=f"+{needed_increase_percent:.1f}%", help=T["to_maintain"])
            st.progress(min(needed_increase_percent/100, 1.0))
            
