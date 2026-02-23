
### Dependency Management

Dependencies are pinned in `requirements.txt` and installed inside Docker.

### Docker Validation

Docker must successfully build and run before any application logic is written.

---

## Phase 1 – Contracts & Specifications

This phase defines **what the system accepts, how it interprets data, and what it guarantees as output**.
No implementation logic is written in this phase.

---

## Supported Input Format

### Supported File Type
- `.xlsx` (Excel)

### Expected Input Columns (as received from bank)

| Column Name   |
|--------------|
| Txn No.      |
| Txn Date     |
| Description  |
| Branch Name  |
| Cheque No.   |
| Dr Amount    |
| Cr Amount    |
| Balance      |

---

## Required vs Optional Columns

### Required Columns

| Column     | Purpose |
|-----------|---------|
| Txn Date  | Transaction date |
| Description | Transaction narration |
| Dr Amount | Expense amount |
| Cr Amount | Income amount |

> At least **one of Dr Amount or Cr Amount must be present per row**

### Optional / Ignored Columns (v1)
- Txn No.
- Branch Name
- Cheque No.
- Balance

These are ignored during processing but may be used in later versions.

---

## Amount Interpretation Rules

The following rules are **strict and deterministic**:

| Condition | Interpretation |
|--------|---------------|
| Dr Amount > 0 | Expense (negative amount) |
| Cr Amount > 0 | Income (positive amount) |
| Both Dr and Cr empty | ❌ Invalid |
| Both Dr and Cr populated | ❌ Invalid |

No AI or heuristics are used for amount interpretation.

---

## Date Handling Rules

- Txn Date must be present
- Must be convertible to a valid date
- Multiple formats are allowed (Excel date, dd-mm-yyyy, dd/mm/yyyy)
- Invalid or missing dates cause the file to be rejected

---

## Row Validation Rules

Each transaction row must satisfy all of the following:

- Txn Date is valid
- Description is not empty
- Exactly one of Dr Amount or Cr Amount is populated
- Amount is greater than zero

### File-Level Rule
- If **any row is invalid**, the entire file is rejected (v1 behavior)

---

## Internal Normalized Data Model

All input bank formats are converted into the following **internal schema**:

| Field | Description |
|----|-------------|
| date | Parsed transaction date |
| description | Cleaned transaction description |
| amount | Signed number (+income, −expense) |
| category | Assigned category |
| flags | HighSpend / None |

All downstream logic operates ONLY on this schema.

---

## Output Contract

### Excel Output (Always Generated)

#### Sheet 1: Transactions
| Column |
|------|
| Date |
| Description |
| Amount |
| Category |
| Flags |

#### Sheet 2: Summary
- Total Income
- Total Expense
- Net Savings
- Highest Spend Category

The output format is stable and consistent across runs.

---

## AI Scope & Boundaries

### AI CAN:
- Read aggregated transaction data
- Generate spending summaries
- Provide financial insights and suggestions

### AI CANNOT:
- Modify Excel files
- Change categories
- Alter calculations
- Override business rules

If AI fails, the Excel output is still generated successfully.

---

## Error Handling Behavior

| Scenario | System Behavior |
|------|----------------|
| Missing required column | Reject file |
| Invalid date | Reject file |
| Invalid Dr/Cr combination | Reject file |
| Empty file | Reject file |
| AI failure | Excel generated, AI skipped |

All errors must be clear and user-readable.

---

## Engineering Principles

- Modular monolith architecture
- Deterministic business rules
- Fail fast and loudly
- Configuration over hardcoding
- AI is additive, not critical

---

## Next Phase

### Phase 2 – Excel Parser Implementation
- Read Excel file
- Validate schema and rows
- Normalize data into internal model
- Add unit tests

---

## Roadmap (Future)
- Budget tracking
- Month-over-month comparison
- Local LLM integration
- Web UI
- Microservice extraction (only if required)