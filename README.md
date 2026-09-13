# 💳 Buy or Wait? — AI Financial Affordability Agent

A high-performance, deterministic AI financial advisor built for the **HackerRank Orchestrate** challenge.

Given a user's purchase or expense inquiry (e.g. *"Can I afford this laptop?"*), the agent reconstructs cash flows, forecasts income and recurring commitments across a 90-day horizon, and recommends the safest course of action while strictly protecting the user's required minimum emergency balance.

---

## 🚀 Quick Start

### 1. Interactive Web Dashboard (Streamlit)
Launch the full visual dashboard with 90-day cash flow charts, preset scenarios, and user profiling:

```powershell
python -m streamlit run code/app.py
```
*Access the dashboard in your browser at [http://localhost:8501](http://localhost:8501)*

### 2. Batch Engine Pipeline
Generate and validate the official 250 predictions in `output.csv`:

```powershell
python code/main.py
```

### 3. CLI Inquiries & Diagnostics
Inspect individual requests with detailed financial diagnostics and stream breakdowns:

```powershell
# Inspect an individual request
python code/main.py --request request_26
python code/main.py --request request_31

# View dataset-wide statistics
python code/main.py --stats
```

---

## 🌟 Interactive UI Features (`code/app.py`)

- **🧮 Custom Expense Simulator ("Can I Afford This?")**:
  - Ask **any custom question** (e.g., *"Can I afford a $800 phone by next month?"*).
  - Select any user profile, configure purchase dates and completion deadlines.
  - Dynamically tweak starting bank balances or emergency buffer floors.
  - Generates instant personalized verdicts, payment plans, and 90-day cash flow simulations.

- **🎛️ Interactive Budget Toggles (Pause Subscriptions Live)**:
  - Discovers flexible expenses (gym, streaming, dining out).
  - Check/uncheck subscriptions to pause them and watch the engine **re-simulate your 90-day cash flow live**.
  - See how pausing non-essential spending unlocks affordability for previously risky purchases.

- **💬 Conversational AI Financial Assistant (Chatbot)**:
  - Ask natural language questions with 1-click quick prompts:
    - 💰 *"What is my max safe spending limit today?"*
    - 📅 *"When is my next salary scheduled to arrive?"*
    - 🧾 *"What are my top recurring monthly bills?"*
    - 🛡️ *"What day will my balance dip to its lowest?"*
  - Instant, mathematically verified answers calculated directly from your transaction ledger and forecast.

- **🎚️ Live Price Sensitivity Slider**:
  - Drag the price slider on any inquiry to test different costs in real time.
  - Instantly reveals whether a price point is 🟢 Safe or 🔴 Unsafe (and by how much).

- **🎯 Clear Plain-English Verdicts**:
  - Large color-coded banners with clear headlines:
    - 🟢 **YES, YOU CAN AFFORD THIS TODAY!**
    - 🔵 **YES, WITH A PAYMENT PLAN!**
    - 🟡 **WAIT UNTIL [DATE] BEFORE BUYING!**
    - 🔴 **NOT RECOMMENDED RIGHT NOW (HIGH RISK)**
  - Snapshot KPIs: Current Balance, Safe Today Limit, Requested Amount, and Emergency Buffer.

- **📈 90-Day Money Journey Chart**:
  - Interactive Altair visualization comparing:
    1. **Projected Balance with Plan**: Account balance under the recommended schedule.
    2. **Emergency Buffer Floor**: Red dashed threshold line.
  - Callouts for the tightest cushion date and lowest forecasted balance.

- **🗂️ Searchable Predictions Table & CSV Export**:
  - Filterable table of all 250 benchmark inquiries with instant search and status filters.
  - One-click `⬇️ Download output.csv` button.


---

## 🧠 System Architecture & Methodology

```
┌─────────────────────────┐
│ Context Ingestion & OCR │  Resolves blank receipt amounts via OCR; parses profiles & FX
└───────────┬─────────────┘
            │
┌───────────▼─────────────────────┐
│ Financial-State Reconstruction  │  Filters failed/cancelled events; converts currencies via dated FX
└───────────┬─────────────────────┘
            │
┌───────────▼─────────────────────┐
│ Recurring-Stream Detection      │  Detects cadences (5, 7, 10, 14, 21, 28–31 days) from history
└───────────┬─────────────────────┘
            │
┌───────────▼─────────────────────┐
│ Message Grounding               │  Applies confirmed salary changes; ignores speculative bonuses
└───────────┬─────────────────────┘
            │
┌───────────▼─────────────────────┐
│ 90-Day Balance Simulation       │  Simulates daily cash flows; verifies balance >= minimum_balance_to_keep
└───────────┬─────────────────────┘
            │
┌───────────▼─────────────────────┐
│ Payment Plan Ranking            │  Ranks full payment, partial, installments, spending cuts, or wait
└───────────┬─────────────────────┘
            │
┌───────────▼─────────────────────┐
│ Deterministic Verifier          │  Validates bounds, chronological order, and CSV specifications
└─────────────────────────────────┘
```

### Evaluation Output Format (`output.csv`):
1. `request_id`: Unique request identifier.
2. `amount_safe_to_pay`: Maximum safe payment today ($0 \le \text{safe} \le \text{requested}$).
3. `affordability_status`: `affordable_now`, `affordable_with_plan`, `affordable_later`, or `not_affordable`.
4. `recommended_payment_method`: `full_payment`, `partial_payment`, `installments`, `wait`, or `not_recommended`.
5. `payment_plan`: Chronological payment schedule (`YYYY-MM-DD:amount|...`) or `none`.
6. `earliest_date_for_full_payment`: Earliest date when paying in full satisfies the 90-day safety check.
7. `spending_changes_needed`: Specific flexible expenses to stop/reduce (`stop:event_id|reduce_to:event_id:amt`) or `none`.
8. `decision_explanation`: Concise, human-understandable explanation supporting the decision.

---

## 📁 Repository Structure

```text
├── README.md                  # Project overview and run guide
├── problem_statement.md       # HackerRank challenge requirements
├── output.csv                 # 250 predictions generated by engine
├── code/
│   ├── main.py                # Core deterministic simulation engine & CLI
│   ├── app.py                 # Interactive Streamlit dashboard
│   ├── analyze_dataset.py     # Dataset distribution explorer
│   └── ...                    # Exploratory & test scripts
├── dataset/                   # Input data files (profiles, events, options, images, FX)
└── evaluation/
    └── usage_report.md        # Token usage and cost report
```
