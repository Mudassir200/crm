<template>
    <div class="finance_discovery" v-if="financial_discovery">
        <div class="expand-btn mb-4">
            <Button :label="buttonLabel" @click="collapse_all = !collapse_all" outlined size="small"></Button>
        </div>
        <div class="fd-panels mb-5 grid lg:grid-cols-3 sm:grid-cols-2 grid-cols-1 gap-4">
            <div>
                <Panel header="Tax Implications" toggleable :collapsed="collapse_all">
                    <div class="fd_table">
                        <table>
                            <tbody>
                                <tr>
                                    <td>Yearly Tax Paid</td>
                                    <td :class="{ 'text-red': financial_discovery.total_tax < 0 }">
                                        {{ formatCurrency(financial_discovery.total_tax) }}</td>
                                </tr>
                                <tr>
                                    <td>Daily Tax Paid</td>
                                    <td :class="{ 'text-red': financial_discovery.total_tax_daily < 0 }">
                                        {{ formatCurrency(financial_discovery.total_tax_daily) }}</td>
                                </tr>
                                <tr>
                                    <td>Months in the year you are working to pay tax</td>
                                    <td>{{ financial_discovery.total_of_month_in_year_for_pay_tax }}</td>
                                </tr>
                                <tr>
                                    <td>Tax Paid Until {{ financial_discovery.retirement_age_goal }} (over the next {{
                                        financial_discovery?.timeframe.toFixed(2) }} years)</td>
                                    <td :class="{ 'text-red': financial_discovery.total_lifetime_tax < 0 }">
                                        {{ formatCurrency(financial_discovery.total_lifetime_tax) }}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </Panel>
            </div>
            <div>
                <Panel header="When will you pay off your home?" toggleable :collapsed="collapse_all">
                    <div class="fd_table">
                        <table>
                            <tbody>
                                <tr>
                                    <td>Current home debt</td>
                                    <td :class="{ 'text-red': financial_discovery.current_home_debt < 0 }">
                                        {{ formatCurrency(financial_discovery.current_home_debt) }}</td>
                                </tr>
                                <tr>
                                    <td>Current monthly payments</td>
                                    <td :class="{ 'text-red': financial_discovery.current_monthly_repayment < 0 }">
                                        {{ formatCurrency(financial_discovery.current_monthly_repayment) }}</td>
                                </tr>
                                <tr>
                                    <td>Current interest rate</td>
                                    <td>{{ financial_discovery.current_interest_rate }}%</td>
                                </tr>
                                <tr>
                                    <td>Years to pay off home</td>
                                    <td>{{ financial_discovery.how_many_years_pay_for_home_free }}</td>
                                </tr>
                                <tr v-for="(buyer, index) in buyers" :key="index">
                                    <td>{{ buyer.title }}</td>
                                    <td>{{ buyer.age || 0 }}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </Panel>
            </div>
            <div>
                <Panel header="Actual Cost of Mortgage" toggleable :collapsed="collapse_all">
                    <div class="fd_table">
                        <table>
                            <tbody>
                                <tr>
                                    <td>Home mortage</td>
                                    <td :class="{ 'text-red': financial_discovery.total_home_mortgage < 0 }">
                                        {{ formatCurrency(financial_discovery.total_home_mortgage) }}</td>
                                </tr>
                                <tr>
                                    <td>Interest liability (still payable)</td>
                                    <td
                                        :class="{ 'text-red': financial_discovery.interest_liability_still_payable < 0 }">
                                        {{ formatCurrency(financial_discovery.interest_liability_still_payable) }}</td>
                                </tr>
                                <tr>
                                    <td>Actual Cost of Mortgage including interest in after tax dollars</td>
                                    <td
                                        :class="{ 'text-red': financial_discovery.actual_cost_of_mortgage_including_interest_after_tax < 0 }">
                                        {{
                                            formatCurrency(financial_discovery.actual_cost_of_mortgage_including_interest_after_tax)
                                        }}
                                    </td>
                                </tr>
                                <tr>
                                    <td>Actual Cost of Mortgage including interest in before tax dollars</td>
                                    <td
                                        :class="{ 'text-red': financial_discovery.actual_cost_of_mortgage_including_interest_before_tax < 0 }">
                                        {{
                                            formatCurrency(financial_discovery.actual_cost_of_mortgage_including_interest_before_tax)
                                        }}
                                    </td>
                                </tr>
                                <tr>
                                    <td>Tax liability on {{ formatCurrency(
                                        financial_discovery.how_many_years_pay_for_home_free) }}
                                        used
                                        to pay
                                        the mortage over {{ financial_discovery.how_many_years_pay_for_home_free }}
                                        years
                                    </td>
                                    <td
                                        :class="{ 'text-red': financial_discovery.tax_liabilities_pay_over_off_years < 0 }">
                                        {{ formatCurrency(financial_discovery.tax_liabilities_pay_over_off_years) }}
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </Panel>
            </div>



        </div>
        <div class="mb-5 grid lg:grid-cols-3 sm:grid-cols-2 grid-cols-1 gap-4">
            <div>
                <Panel header="Where does your money go?" toggleable :collapsed="collapse_all">
                    <div class="fd_table">
                        <table>
                            <tbody>
                                <tr>
                                    <td>Total Gross Annual Income</td>
                                    <td :class="{ 'text-red': financial_discovery.total_gross_annual_income < 0 }">
                                        {{ formatCurrency(financial_discovery.total_gross_annual_income) }}</td>
                                </tr>
                                <tr>
                                    <td>Total Annual Tax</td>
                                    <td :class="{ 'text-red': financial_discovery.total_tax < 0 }">
                                        {{ formatCurrency(financial_discovery.total_tax) }}</td>
                                </tr>
                                <tr>
                                    <td>Total Annual Mortgage Payments</td>
                                    <td :class="{ 'text-red': financial_discovery.total_annual_mortgage_payments < 0 }">
                                        {{ formatCurrency(financial_discovery.total_annual_mortgage_payments) }}</td>
                                </tr>
                                <tr>
                                    <td>Total Net Annual Income</td>
                                    <td :class="{ 'text-red': financial_discovery.total_net_annual_income < 0 }">
                                        {{ formatCurrency(financial_discovery.total_net_annual_income) }}
                                    </td>
                                </tr>
                                <tr>
                                    <td>Portion of income going to tax and mortage</td>
                                    <td>{{ financial_discovery.portion_of_income_going_to_tax_and_mortgage }}%</td>
                                </tr>
                                <tr>
                                    <td>The day of the year when you start making money for yourself</td>
                                    <td>{{ financial_discovery.day_of_year_when_start_making_money }}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </Panel>
            </div>
            <div>
                <Panel header="Savings Required" toggleable :collapsed="collapse_all">
                    <div class="fd_table">
                        <table>
                            <tbody>
                                <tr>
                                    <td>Current eldest age</td>
                                    <td>{{ financial_discovery.current_eldest_age }}</td>
                                </tr>
                                <tr>
                                    <td>Retirement age goal</td>
                                    <td>{{ financial_discovery.retirement_age_goal }}</td>
                                </tr>
                                <tr>
                                    <td>Years until retirement (based on current eldest age)</td>
                                    <td>{{ financial_discovery.years_until_retirement }}</td>
                                </tr>
                                <tr>
                                    <td>Yearly savings required starting today</td>
                                    <td
                                        :class="{ 'text-red': financial_discovery.yearly_savings_required_starting_today < 0 }">
                                        {{ formatCurrency(financial_discovery.yearly_savings_required_starting_today) }}
                                    </td>
                                </tr>
                                <tr>
                                    <td>Daily savings required starting today (for the next {{ days_for_free }} days)
                                    </td>
                                    <td
                                        :class="{ 'text-red': financial_discovery.daily_savings_required_starting_today < 0 }">
                                        {{ formatCurrency(financial_discovery.daily_savings_required_starting_today) }}
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </Panel>
            </div>
            <div>
                <Panel header="Retirement Goal Adjustment" toggleable :collapsed="collapse_all">
                    <div class="fd_table">
                        <table>
                            <tbody>
                                <tr>
                                    <td>Retirement age goal</td>
                                    <td>{{ financial_discovery.retirement_age_goal }}</td>
                                </tr>
                                <tr>
                                    <td>Annual Retirement Income Goal</td>
                                    <td :class="{ 'text-red': financial_discovery.annual_income_goal < 0 }">
                                        {{ formatCurrency(financial_discovery.annual_income_goal) }}
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </Panel>
            </div>
        </div>

        <div class="fd_summary-table">
            <div class="grid-item item1">
                <Panel header="Summary" toggleable :collapsed="collapse_all">
                    <div class="fd_table grid lg:grid-cols-2 grid-cols-1 gap-5 items-end">
                        <table class="table bg-white border border-gray-300">
                            <thead>
                                <tr>
                                    <td
                                        class="px-6 py-3 border border-gray-300 text-left text-md font-bold tracking-wider">
                                        Assets
                                    </td>
                                    <td
                                        class="px-6 py-3 border border-gray-300 text-left text-md font-bold tracking-wider">
                                        Current
                                    </td>
                                    <td
                                        class="px-6 py-3 border border-gray-300 text-left text-md font-bold tracking-wider">
                                        Projection ({{ financial_discovery?.timeframe.toFixed(2) }}yrs)
                                    </td>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td class="px-6 py-4 border border-gray-300">
                                        <div style=" display: flex;align-items: center;justify-content: space-between;">
                                            <span class="mr-3">Investment property</span>
                                            <InputNumber v-model="annual_growth.property_investment"
                                                inputId="annual_growth" suffix="%" fluid :minFractionDigits="0"
                                                :maxFractionDigits="2" :invalid="!annual_growth.property_investment"
                                                :min="0" :max="100" style="width: 62px;"
                                                v-tooltip.top="'Annual Growth of Investment Property'" />
                                        </div>
                                    </td>
                                    <td class="px-6 py-4 border border-gray-300"
                                        :class="{ 'text-red': financial_discovery.investment_property_current < 0 }">
                                        {{ formatCurrency(financial_discovery.investment_property_current) }}
                                    </td>
                                    <td class="px-6 py-4 border border-gray-300"
                                        :class="{ 'text-red': financial_discovery.investment_property_after_projection_year < 0 }">
                                        {{
                                            formatCurrency(financial_discovery.investment_property_after_projection_year)
                                        }}
                                    </td>
                                </tr>
                                <tr>
                                    <td class="px-6 py-4 border border-gray-300">
                                        <div style=" display: flex;align-items: center;justify-content: space-between;">
                                            <span class="mr-3">Superannuation</span>
                                            <InputNumber v-model="annual_growth.superannuation" inputId="annual_growth"
                                                suffix="%" fluid :minFractionDigits="0" :maxFractionDigits="2"
                                                :invalid="!annual_growth.superannuation" :min="0" :max="100"
                                                style="width: 62px;"
                                                v-tooltip.top="'Annual Growth of Superannuation'" />
                                        </div>
                                    </td>
                                    <td class="px-6 py-4 border border-gray-300"
                                        :class="{ 'text-red': financial_discovery.superannuation_current < 0 }">
                                        {{ formatCurrency(financial_discovery.superannuation_current) }}
                                    </td>
                                    <td class="px-6 py-4 border border-gray-300"
                                        :class="{ 'text-red': financial_discovery.superannuation_after_projection_year < 0 }">
                                        {{ formatCurrency(financial_discovery.superannuation_after_projection_year) }}
                                    </td>
                                </tr>
                                <tr>
                                    <td class="px-6 py-4 border border-gray-300">
                                        <div class="flex items-center justify-between">
                                            <span>Cash savings</span>
                                            <InputNumber v-model="annual_growth.cash_savings" inputId="annual_growth"
                                                suffix="%" fluid :minFractionDigits="0" :maxFractionDigits="2"
                                                :invalid="!annual_growth.cash_savings" :min="0" :max="100"
                                                style="width: 62px;" v-tooltip.top="'Annual Growth of Cash savings'" />
                                        </div>

                                    </td>
                                    <td class="px-6 py-4 border border-gray-300"
                                        :class="{ 'text-red': financial_discovery.cash_savings_current < 0 }">
                                        {{ formatCurrency(financial_discovery.cash_savings_current) }}
                                    </td>
                                    <td class="px-6 py-4 border border-gray-300"
                                        :class="{ 'text-red': financial_discovery.cash_savings_after_projection_year < 0 }">
                                        {{ formatCurrency(financial_discovery.cash_savings_after_projection_year) }}
                                    </td>
                                </tr>
                                <tr>
                                    <td class="px-6 py-4 border border-gray-300">
                                        <div class="flex items-center justify-between">
                                            <span>Shares & Equities</span>
                                            <InputNumber v-model="annual_growth.shares_equities" inputId="annual_growth"
                                                suffix="%" fluid :minFractionDigits="0" :maxFractionDigits="2"
                                                :invalid="!annual_growth.shares_equities" :min="0" :max="100"
                                                style="width: 62px;"
                                                v-tooltip.top="'Annual Growth of Shares & Equities'" />
                                        </div>
                                    </td>
                                    <td class="px-6 py-4 border border-gray-300"
                                        :class="{ 'text-red': financial_discovery.others_current < 0 }">
                                        {{ formatCurrency(financial_discovery.others_current) }}
                                    </td>
                                    <td class="px-6 py-4 border border-gray-300"
                                        :class="{ 'text-red': financial_discovery.others_after_projection_year < 0 }">
                                        {{ formatCurrency(financial_discovery.others_after_projection_year) }}
                                    </td>
                                </tr>
                                <tr>
                                    <td
                                        class="px-6 py-3 border border-gray-300 text-left text-md font-bold tracking-wider">
                                        Total Assets
                                    </td>
                                    <td class="px-6 py-3 border border-gray-300 text-left text-md font-bold tracking-wider"
                                        :class="{ 'text-red': financial_discovery.total_assets_current < 0 }">
                                        {{ formatCurrency(financial_discovery.total_assets_current) }}
                                    </td>
                                    <td class="px-6 py-3 border border-gray-300 text-left text-md font-bold tracking-wider"
                                        :class="{ 'text-red': financial_discovery.total_assets__after_projection_year < 0 }">
                                        {{ formatCurrency(financial_discovery.total_assets__after_projection_year) }}
                                    </td>
                                </tr>
                                <tr>
                                    <td colspan="3"
                                        class="px-6 py-3 border border-gray-300 text-left text-md font-bold tracking-wider">
                                        Liabilities
                                    </td>
                                </tr>
                                <tr>
                                    <td class="px-6 py-4 border border-gray-300">
                                        PPOR Debt
                                    </td>
                                    <td class="px-6 py-4 border border-gray-300"
                                        :class="{ 'text-red': financial_discovery.home_mortgage_current < 0 }">
                                        {{ formatCurrency(financial_discovery.home_mortgage_current) }}
                                    </td>
                                    <td class="px-6 py-4 border border-gray-300"
                                        :class="{ 'text-red': financial_discovery.home_mortgage_after_projection_year < 0 }">
                                        {{ formatCurrency(financial_discovery.home_mortgage_after_projection_year) }}
                                    </td>
                                </tr>
                                <tr>
                                    <td class="px-6 py-4 border border-gray-300">
                                        Investment Property Debt
                                    </td>
                                    <td class="px-6 py-4 border border-gray-300"
                                        :class="{ 'text-red': financial_discovery.liabilities_investment_property_current < 0 }">
                                        {{ formatCurrency(financial_discovery.liabilities_investment_property_current)
                                        }}
                                    </td>
                                    <td class="px-6 py-4 border border-gray-300"
                                        :class="{ 'text-red': financial_discovery.liabilities_investment_property_after_projection_year < 0 }">
                                        {{ formatCurrency(
                                            financial_discovery.liabilities_investment_property_after_projection_year) }}
                                    </td>
                                </tr>
                                <tr>
                                    <td class="px-6 py-4 border border-gray-300">
                                        Other debt
                                    </td>
                                    <td class="px-6 py-4 border border-gray-300"
                                        :class="{ 'text-red': financial_discovery.other_debt_current < 0 }">
                                        {{ formatCurrency(financial_discovery.other_debt_current) }}
                                    </td>
                                    <td class="px-6 py-4 border border-gray-300"
                                        :class="{ 'text-red': financial_discovery.other_debt_after_projection_year < 0 }">
                                        -
                                        <!-- {{ formatCurrency(financial_discovery.other_debt_after_projection_year) }} -->
                                    </td>
                                </tr>
                                <tr>
                                    <td
                                        class="px-6 py-3 border border-gray-300 text-left text-md font-bold tracking-wider">
                                        Total Liabilities
                                    </td>
                                    <td class="px-6 py-3 border border-gray-300 text-left text-md font-bold tracking-wider"
                                        :class="{ 'text-red': financial_discovery.total_liabilities_current < 0 }">
                                        {{ formatCurrency(financial_discovery.total_liabilities_current) }}
                                    </td>
                                    <td class="px-6 py-3 border border-gray-300 text-left text-md font-bold tracking-wider"
                                        :class="{ 'text-red': financial_discovery.total_liabilities_after_projection_year < 0 }">
                                        {{ formatCurrency(financial_discovery.total_liabilities_after_projection_year)
                                        }}
                                    </td>
                                </tr>
                                <tr>
                                    <td colspan="3"
                                        class="px-6 py-3 border border-gray-300 text-left text-md font-bold tracking-wider">
                                    </td>
                                </tr>
                                <tr>
                                    <td
                                        class="px-6 py-3 border border-gray-300 text-left text-md font-bold tracking-wider">
                                        Net Wealth
                                    </td>
                                    <td class="px-6 py-3 border border-gray-300 text-left text-md font-bold tracking-wider"
                                        :class="{ 'text-red': financial_discovery.net_wealth_current < 0 }">
                                        {{ formatCurrency(financial_discovery.net_wealth_current) }}
                                    </td>
                                    <td class="px-6 py-3 border border-gray-300 text-left text-md font-bold tracking-wider"
                                        :class="{ 'text-red': financial_discovery.net_wealth_after_projection_year < 0 }">
                                        {{ formatCurrency(financial_discovery.net_wealth_after_projection_year) }}
                                    </td>
                                </tr>
                                <tr>
                                    <td colspan="3"
                                        class="px-6 py-3 border border-gray-300 text-left text-md font-bold tracking-wider">
                                    </td>
                                </tr>
                                <tr>
                                    <td class="px-6 py-4 border border-gray-300">
                                        Retirement Income Method
                                    </td>
                                    <td class="px-6 py-4 border border-gray-300">
                                        {{ financial_discovery.retirement_income_method }}
                                    </td>
                                    <td class="px-6 py-4 border border-gray-300">
                                        -
                                    </td>
                                </tr>
                                <tr>
                                    <td class="px-6 py-4 border border-gray-300">
                                        Retirement Age Goal
                                    </td>
                                    <td class="px-6 py-4 border border-gray-300">
                                        {{ financial_discovery.retirement_age_goal }}
                                    </td>
                                    <td class="px-6 py-4 border border-gray-300">
                                        -
                                    </td>
                                </tr>
                                <tr>
                                    <td class="px-6 py-4 border border-gray-300">
                                        Timeframe
                                    </td>
                                    <td class="px-6 py-4 border border-gray-300">
                                        {{ financial_discovery.timeframe.toFixed(2) }}
                                    </td>
                                    <td class="px-6 py-4 border border-gray-300">
                                        -
                                    </td>
                                </tr>
                                <tr>
                                    <td class="px-6 py-4 border border-gray-300">
                                        Years Retired (up to {{ financial_discovery.life_expectancy }})
                                    </td>
                                    <td class="px-6 py-4 border border-gray-300">
                                        {{ financial_discovery.years_retired_up_to_life_expectancy }}
                                    </td>
                                    <td class="px-6 py-4 border border-gray-300">
                                        -
                                    </td>
                                </tr>
                                <tr>
                                    <td class="px-6 py-4 border border-gray-300">
                                        Annual retirement income goal
                                    </td>
                                    <td class="px-6 py-4 border border-gray-300"
                                        :class="{ 'text-red': financial_discovery.annual_income_goal < 0 }">
                                        {{ formatCurrency(financial_discovery.annual_income_goal) }}
                                    </td>
                                    <td class="px-6 py-4 border border-gray-300">
                                        -
                                    </td>
                                </tr>
                                <tr>
                                    <td class="px-6 py-4 border border-gray-300 text-md font-bold tracking-wider">
                                        Lump sum needed in {{ current_year }} dollars
                                    </td>
                                    <td class="px-6 py-4 text-yellow border border-gray-300 text-md font-bold tracking-wider"
                                        :class="{ 'text-red': financial_discovery.lump_sum_needed < 0 }">
                                        {{ formatCurrency(financial_discovery.lump_sum_needed) }}
                                    </td>
                                    <td class="px-6 py-4 border border-gray-300 text-md font-bold tracking-wider">
                                        -
                                    </td>
                                </tr>
                                <tr>
                                    <td class="px-6 py-4 border border-gray-300">
                                        Lump sum needed (inflation adjusted)
                                    </td>
                                    <td class="px-6 py-4 border border-gray-300"
                                        :class="{ 'text-red': financial_discovery.lump_sum_needed_inflation_adjusted < 0 }">
                                        {{ formatCurrency(financial_discovery.lump_sum_needed_inflation_adjusted) }}
                                    </td>
                                    <td class="px-6 py-4 border border-gray-300">
                                        -
                                    </td>
                                </tr>
                                <tr>
                                    <td class="px-6 py-4 border border-gray-300 text-md font-bold tracking-wider">
                                        Retirement shortfall including inflation
                                    </td>
                                    <td class="px-6 py-4 border border-gray-300 text-md font-bold tracking-wider"
                                        :class="{ 'text-red': financial_discovery.retirement_shortfall_including_inflation_current < 0 }">
                                        {{
                                            formatCurrency(financial_discovery.retirement_shortfall_including_inflation_current)
                                        }}
                                    </td>
                                    <td class="px-6 py-4 border border-gray-300 text-md font-bold tracking-wider"
                                        :class="{ 'text-red': financial_discovery.retirement_shortfall_including_inflation_after_projection_year < 0 }">
                                        {{
                                            formatCurrency(financial_discovery.retirement_shortfall_including_inflation_after_projection_year)
                                        }}
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        <div>
                            <table class="table-small">
                                <tbody>
                                    <tr>
                                        <td>Average annual inflation rate</td>
                                        <td class="w-[62px]">
                                            <InputNumber v-model="average_annual_inflation_rate"
                                                inputId="average_annual_inflation_rate" suffix="%"
                                                inputClass="w-full max-w-[62px]" :minFractionDigits="0"
                                                :maxFractionDigits="2" :invalid="!average_annual_inflation_rate"
                                                :min="0" :max="100" v-tooltip.top="'Average annual inflation rate'" />
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>Passive income rate of return in retirement</td>
                                        <td class="w-[62px]">
                                            <InputNumber v-model="passive_income_rate_of_return_in_retirement"
                                                inputId="passive_income_rate_of_return_in_retirement" suffix="%"
                                                inputClass="w-full max-w-[62px]" :minFractionDigits="0"
                                                :maxFractionDigits="2"
                                                :invalid="!passive_income_rate_of_return_in_retirement" :min="0"
                                                :max="100" style="width: 62px;"
                                                v-tooltip.top="'Passive income rate of return in retirement'" />
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>Life expectancy</td>
                                        <td class="w-[62px]">
                                            <InputNumber v-model="life_expectancy" inputId="life_expectancy"
                                                inputClass="w-full max-w-[62px]" :minFractionDigits="0"
                                                :maxFractionDigits="2" :invalid="!life_expectancy" :min="0"
                                                style="width: 62px;" v-tooltip.top="'Life expectancy'" />
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </Panel>
            </div>

        </div>
    </div>
</template>
<script>

import { currencyFormat, fetch_api } from '@/utils'
import Button from 'primevue/button';

export default {
    name: "FinanceDiscovery",
    components: {
        Button
    },
    data() {
        return {
            financial_discovery: false,
            buyers: [],
            current_year: 2024,
            days_for_free: 0,
            propertyGrowth: 0,
            annualGrowth: 0,
            collapse_all: true,
            annual_growth: {
                superannuation: 0,
                cash_savings: 0,
                shares_equities: 0,
                property_investment: 0,
            },
            average_annual_inflation_rate: 0,
            passive_income_rate_of_return_in_retirement: 0,
            life_expectancy: 0
        }
    },
    watch: {
        'financial_discovery': function (data) {
            this.buyers = []
            if (data.buyers.length > 0) {
                data.buyers.forEach(buyer => {
                    this.buyers.push({
                        title: `${buyer.first_name} ${buyer.surname}'s age when PPOR debt free`,
                        age: parseInt(buyer.age) + parseInt(data.how_many_years_pay_for_home_free)
                    })
                });
            }

            this.days_for_free = parseInt(data.years_until_retirement) * 365
            this.annual_growth.property_investment = data.annual_growth_of_investment_property
            this.annual_growth.superannuation = data.annual_growth_of_superannuation
            this.annual_growth.cash_savings = data.annual_growth_of_cash_savings
            this.annual_growth.shares_equities = data.annual_growth_of_share_equities
            this.average_annual_inflation_rate = data.average_annual_inflation_rate
            this.passive_income_rate_of_return_in_retirement = data.passive_income_rate_of_return_in_retirement
            this.life_expectancy = data.life_expectancy
        },
        'annual_growth.property_investment': function (data) {
            if (data !== this.financial_discovery.annual_growth_of_investment_property && data > 0 && data <= 100) {
                this.updateAnnualGrowth_of_prop_investment();
            }
        },
        'annual_growth.superannuation': function (data) {
            if (data !== this.financial_discovery.annual_growth_of_superannuation && data > 0 && data <= 100) {
                this.updateAnnualGrowth_of_superannuation();
            }
        },
        'annual_growth.cash_savings': function (data) {
            if (data !== this.financial_discovery.annual_growth_of_cash_savings && data > 0 && data <= 100) {
                this.updateAnnualGrowth_of_cash_savings();
            }
        },
        'annual_growth.shares_equities': function (data) {
            if (data !== this.financial_discovery.annual_growth_of_share_equities && data > 0 && data <= 100) {
                this.updateAnnualGrowth_of_share_equities();
            }
        },
        'average_annual_inflation_rate': function (data) {
            if (data !== this.financial_discovery.average_annual_inflation_rate && data > 0 && data <= 100) {
                this.updateAverage_annual_inflation_rate();
            }
        },
        'passive_income_rate_of_return_in_retirement': function (data) {
            if (data !== this.financial_discovery.passive_income_rate_of_return_in_retirement && data > 0 && data <= 100) {
                this.updatePassive_income_rate_of_return_in_retirement();
            }
        },
        'life_expectancy': function (data) {
            if (data !== this.financial_discovery.life_expectancy) {
                this.updateLife_expectancy();
            }
        },
    },
    computed: {
        buttonLabel() {
            return this.collapse_all ? 'Expand All' : 'Collapse All';
        }
    },
    async mounted() {
        await this.getData();
        this.current_year = new Date().getFullYear()
    },    
    methods: {
        async getData() {
            let params = {
                fdId: this.$route.params.id
            }
            let url = "/api/method/crm.financial_discovery.api.financial_discovery.calculateAllFDFields"
            let res = await fetch_api(url, "POST", params);
            if (res.message?.name) {
                this.financial_discovery = res.message;
            } else {
                this.financial_discovery = false;
                this.$toast.add({ severity: 'error', summary: 'Error', detail: res?.message, life: 5000 });
            }
        },
        formatCurrency(value) {
            return currencyFormat(Math.round(value))
        },
        async updateAnnualGrowth_of_prop_investment() {
            let url = "/api/method/crm.financial_discovery.api.financial_discovery.updateAnnualGrowth_of_prop_investment"
            let res = await fetch_api(url, "POST", {
                id: this.$route.params.id,
                rate: this.annual_growth.property_investment
            })

            if (res.message?.name) {
                this.getData();
                this.$toast.add({ severity: 'success', summary: 'Success', detail: 'Property Investment Annual Growth update successfully.', life: 5000 });
            } else {
                this.$toast.add({ severity: 'error', summary: 'Error', detail: res.message, life: 5000 });
            }
        },
        async updateAnnualGrowth_of_superannuation() {
            let url = "/api/method/crm.financial_discovery.api.financial_discovery.updateAnnualGrowth_of_superannuation"
            let res = await fetch_api(url, "POST", {
                id: this.$route.params.id,
                rate: this.annual_growth.superannuation
            })

            if (res.message?.name) {
                this.getData();
                this.$toast.add({ severity: 'success', summary: 'Success', detail: 'Superannuation Annual Growth update successfully.', life: 5000 });
            } else {
                this.$toast.add({ severity: 'error', summary: 'Error', detail: res.message, life: 5000 });
            }
        },
        async updateAnnualGrowth_of_cash_savings() {
            let url = "/api/method/crm.financial_discovery.api.financial_discovery.updateAnnualGrowth_of_cash_savings"
            let res = await fetch_api(url, "POST", {
                id: this.$route.params.id,
                rate: this.annual_growth.cash_savings
            })

            if (res.message?.name) {
                this.getData();
                this.$toast.add({ severity: 'success', summary: 'Success', detail: 'Cash Savings Annual Growth update successfully.', life: 5000 });
            } else {
                this.$toast.add({ severity: 'error', summary: 'Error', detail: res.message, life: 5000 });
            }
        },
        async updateAnnualGrowth_of_share_equities() {
            let url = "/api/method/crm.financial_discovery.api.financial_discovery.updateAnnualGrowth_of_share_equities"
            let res = await fetch_api(url, "POST", {
                id: this.$route.params.id,
                rate: this.annual_growth.shares_equities
            })

            if (res.message?.name) {
                this.getData();
                this.$toast.add({ severity: 'success', summary: 'Success', detail: 'Shares & Equities Annual Growth update successfully.', life: 5000 });
            } else {
                this.$toast.add({ severity: 'error', summary: 'Error', detail: res.message, life: 5000 });
            }
        },
        async updateAverage_annual_inflation_rate() {
            let url = "/api/method/crm.financial_discovery.api.financial_discovery.updateAverage_annual_inflation_rate"
            let res = await fetch_api(url, "POST", {
                id: this.$route.params.id,
                rate: this.average_annual_inflation_rate
            })

            if (res.message?.name) {
                this.getData();
                this.$toast.add({ severity: 'success', summary: 'Success', detail: 'Average annual inflation rate update successfully.', life: 5000 });
            } else {
                this.$toast.add({ severity: 'error', summary: 'Error', detail: res.message, life: 5000 });
            }
        },
        async updatePassive_income_rate_of_return_in_retirement() {
            let url = "/api/method/crm.financial_discovery.api.financial_discovery.updatePassive_income_rate_of_return_in_retirement"
            let res = await fetch_api(url, "POST", {
                id: this.$route.params.id,
                rate: this.passive_income_rate_of_return_in_retirement
            })

            if (res.message?.name) {
                this.getData();
                this.$toast.add({ severity: 'success', summary: 'Success', detail: 'Passive income rate of return in retirement update successfully.', life: 5000 });
            } else {
                this.$toast.add({ severity: 'error', summary: 'Error', detail: res.message, life: 5000 });
            }
        },
        async updateLife_expectancy() {
            let url = "/api/method/crm.financial_discovery.api.financial_discovery.updateLife_expectancy"
            let res = await fetch_api(url, "POST", {
                id: this.$route.params.id,
                rate: this.life_expectancy
            })

            if (res.message?.name) {
                this.getData();
                this.$toast.add({ severity: 'success', summary: 'Success', detail: 'Life expectancy update successfully.', life: 5000 });
            } else {
                this.$toast.add({ severity: 'error', summary: 'Error', detail: res.message, life: 5000 });
            }
        },
    },
}
</script>

<style>
.finance_discovery .grid-container {
    display: grid;
    grid-template-columns: repeat(12, 1fr) !important;
    gap: 20px;
}

.grid-item.item1 {
    grid-column: span 6;
}

.grid-item.item2 {
    grid-column: span 6;
}

@media only screen and (max-width: 768px) {
    .grid-item.item1 {
        grid-column: span 12;
    }

    .grid-item.item2 {
        grid-column: span 12;
    }
}

.finance_discovery input {
    padding: 6px 8px;
    box-shadow: none;
    font-size: 14px;
}

.text-red {
    color: red;
}

.text-yellow {
    background: yellow;
    color: #000;
}

.finance_discovery .fd_table table {
    border: 1px solid #e2e8f0;
    border-collapse: collapse;
    width: 100%;
}

.finance_discovery .fd_table table tr:not(:last-child) {
    border-bottom: 1px solid #e2e8f0;
}

.finance_discovery .fd_table table tr td:not(:last-child) {
    border-right: 1px solid #e2e8f0;
}

.finance_discovery .fd_table table tr td {
    padding: 5px 10px;
}

.finance_discovery .fd_summary-table .p-panel .p-panel-content-container {
    overflow: auto;
}

.finance_discovery .fd_tables {
    display: grid;
    gap: 20px;
}

.finance_discovery .fd_tables .fd_table .table-title {
    margin-bottom: 10px;
}

.finance_discovery .fd_tables .fd_table table {
    border: 1px solid #e2e8f0;
    border-collapse: collapse;
    width: 100%;
}

.finance_discovery .fd_tables .fd_table table>tr:not(:last-child) {
    border-bottom: 1px solid #e2e8f0;
}

.finance_discovery .fd_tables .fd_table table tr>td:not(:last-child) {
    border-right: 1px solid #e2e8f0;
}

.finance_discovery .fd_tables .fd_table table tr>td {
    padding: 5px 10px;
}

@media(min-width: 540px) {
    .finance_discovery .fd_tables {
        grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
    }
}
</style>