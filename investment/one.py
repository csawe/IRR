property_value_list = []
loan_amount_list = []
equity_list = []
gross_rental_income_list = []
loan_principle_list = []
loan_interest_list = []
total_loan_payment_list = []
additional_loan_payment_list = []
renovations_own_list = []
renovations_loan_list = []
repairs_and_maintenance_list = []
special_expenses_list = []
property_expenses_list = []
total_property_expenses_list = []
capital_received_list = []
pre_tax_cashflow_list = []
initial_capital_outflow_list = []
pre_tax_cashoncash_list = []
total_taxable_deductions_list = []
depreciation_list = []
taxable_amaount_list = []
tax_credit_list = []
after_tax_cashflow_list = []
after_tax_cashoncash_list = []
income_per_month_list_list = []
irr_list = []

temp.determine_property_value()
temp.assign_interest_rates()
temp.determine_outstanding_loan_per_year()
temp.determine_equity_per_year()
temp.determine_gross_rental_income()
temp.determine_loan_interest()
temp.determine_loan_principal()
temp.determine_total_loan_payment()
temp.determine_repairs_and_maintenance()
temp.determine_special_expenses()
temp.determine_property_expenses_per_year()
temp.determine_total_property_expenses_per_year()
temp.determine_pre_tax_cash_flow_per_year()
temp.determine_initial_capital_outflow_per_year()
temp.determine_pre_tax_cash_on_cash()
temp.determine_taxable_deductions()
temp.assign_depreciation()
temp.calculate_taxable_amount()
temp.determine_tax_credits()
temp.determine_after_tax_cashflow()
temp.determine_after_tax_cash_on_cash()
temp.determine_income_per_month()

self.assign_property_value()
self.assign_outstanding_loan()
self.assign_equity()
self.assign_gross_rental_income()
self.assign_loan_interest()
self.assign_loan_principle()
self.assign_total_loan_payment()
self.assign_additional_loan_payments()
self.assign_renovations_own()
self.assign_renovations_loan()
self.assign_repairs_and_maintenance()
self.assign_special_expenses()
self.assign_property_expenses()
self.assign_total_property_expenses()
self.assign_capital_list()
self.assign_pre_tax_cashflow()
self.assign_initial_capital_outflow()
self.assign_pre_tax_cashoncash()
self.assign_taxable_deductions()
self.assign_depreciation()
self.assign_taxable_amount()
self.assign_tax_credits()
self.assign_after_tax_cashflow()
self.assign_after_tax_cashoncash()
self.assign_income()
self.assign_irr()