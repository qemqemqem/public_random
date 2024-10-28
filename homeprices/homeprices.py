import argparse

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Calculate and compare NPV of buying vs renting a home'
    )

    # Required arguments
    parser.add_argument('--home-price', type=float, default=1320600,
                      help='Home price in dollars (e.g. 1320600)')
    parser.add_argument('--rent', type=float, default=2600,
                      help='Monthly rent in dollars (e.g. 2600)')

    # Optional arguments with defaults
    parser.add_argument('--down-payment-rate', type=float, default=0.20,
                      help='Down payment as percentage of home price (default: 0.20)')
    parser.add_argument('--mortgage-rate', type=float, default=0.065,
                      help='Annual mortgage interest rate (default: 0.065)')
    parser.add_argument('--mortgage-term', type=int, default=30,
                      help='Mortgage term in years (default: 30)')
    parser.add_argument('--occupation-length', type=int, default=6,
                      help='Expected years of occupation (default: 6)')
    parser.add_argument('--appreciation-rate', type=float, default=0.056,
                      help='Annual home appreciation rate (default: 0.056)')
    parser.add_argument('--investment-return', type=float, default=0.05,
                      help='Expected investment return rate (default: 0.05)')
    parser.add_argument('--stock-market-return', type=float, default=0.06,
                      help='Expected stock market return rate (default: 0.06)')
    parser.add_argument('--maintenance-cost-rate', type=float, default=0.015,
                      help='Annual maintenance cost as percentage of home value (default: 0.015)')
    parser.add_argument('--tax-rate', type=float, default=0.0079,
                      help='Property tax rate (default: 0.0079)')
    parser.add_argument('--closing-cost-rate', type=float, default=0.03,
                      help='Closing costs as percentage of home price (default: 0.03)')
    parser.add_argument('--selling-cost-rate', type=float, default=0.03,
                      help='Selling costs as percentage of home price (default: 0.06)')

    args = parser.parse_args()

    # Calculate derived values
    args.down_payment = args.home_price * args.down_payment_rate
    args.closing_costs = args.home_price * args.closing_cost_rate

    return args

def calculate_stock_investment(initial_investment, annual_contribution, years, return_rate, investment_return):
    """Calculate the future value of stock market investments

    Args:
        initial_investment: Initial amount invested
        annual_contribution: Annual additional investment
        years: Investment horizon
        return_rate: Expected annual return rate
        investment_return: Rate used for NPV calculations
    """
    value = initial_investment
    npv = -initial_investment  # Initial investment is a negative cash flow

    print("\nStock Market Investment:")
    print(f"Initial investment: ${initial_investment:,.2f}")
    print(f"Annual contribution: ${annual_contribution:,.2f}")

    for year in range(1, years + 1):
        # Add annual contribution at start of year
        value = value * (1 + return_rate) + annual_contribution
        # Calculate NPV of contribution
        contribution_npv = -annual_contribution / ((1 + investment_return) ** year)
        npv += contribution_npv

    # Calculate NPV of final value
    final_value_npv = value / ((1 + investment_return) ** years)
    npv += final_value_npv

    print(f"Year {years} - Final Value: ${value:,.2f}")
    print(f"NPV of Investment: ${npv:,.2f}")

    return npv

def calculate_npv_renting(monthly_rent, occupation_length, investment_return, rent_increase_rate=0.03):
    """Calculate the NPV of renting for a given period

    Args:
        monthly_rent: Initial monthly rent
        occupation_length: Number of years to rent
        rent_increase_rate: Annual rate of rent increase (default 3%)
    """
    npv_rent = 0
    annual_rent = monthly_rent * 12

    print("\nRental cash flows:")
    print(f"Initial annual rent: ${annual_rent:,.2f}")

    for year in range(1, occupation_length + 1):
        # Calculate rent for this year with annual increases
        year_rent = annual_rent * ((1 + rent_increase_rate) ** (year - 1))
        discounted_rent = -year_rent / ((1 + investment_return) ** year)
        print(f"Year {year} - Rent: ${year_rent:,.2f}, Discounted: ${discounted_rent:,.2f}")
        npv_rent += discounted_rent

    return npv_rent

def calculate_npv_buying(home_price, down_payment, mortgage_rate, mortgage_term,
                         occupation_length, appreciation_rate, maintenance_cost_rate,
                         tax_rate, closing_costs, selling_cost_rate, investment_return):
    # Initial costs are always negative
    npv_buy = -down_payment - closing_costs

    # If selling immediately, only consider purchase costs and immediate sale
    if occupation_length == 0:
        final_home_value = home_price
        selling_costs = selling_cost_rate * final_home_value
        return npv_buy - selling_costs

    # Calculate annual mortgage payment
    mortgage_payment = (home_price - down_payment) * (mortgage_rate / 12) / \
                       (1 - (1 + mortgage_rate / 12) ** (-mortgage_term * 12)) * 12
    maintenance = maintenance_cost_rate * home_price
    property_tax = tax_rate * home_price

    # Calculate annual cash flows
    print("\nAnnual cash flows:")
    print(f"Annual mortgage payment: ${mortgage_payment:,.2f}")
    print(f"Annual maintenance: ${maintenance:,.2f}")
    print(f"Annual property tax: ${property_tax:,.2f}")

    for year in range(1, occupation_length + 1):
        # Annual costs are always negative
        annual_costs = -(mortgage_payment + maintenance + property_tax)
        discounted_costs = annual_costs / ((1 + investment_return) ** year)
        print(f"Year {year} - Costs: ${annual_costs:,.2f}, Discounted: ${discounted_costs:,.2f}")
        npv_buy += discounted_costs

    # Calculate remaining mortgage balance using amortization
    # P(1+r)^n - P(r(1+r)^n)/((1+r)^n - 1) where P is principal, r is monthly rate, n is months
    r = mortgage_rate / 12
    n = occupation_length * 12
    initial_mortgage = home_price - down_payment
    remaining_mortgage = initial_mortgage * (1 + r)**n - \
                        initial_mortgage * (r * (1 + r)**n) / ((1 + r)**n - 1)

    # Account for selling the property at the end of occupation
    final_home_value = home_price * ((1 + appreciation_rate) ** occupation_length)
    selling_costs = selling_cost_rate * final_home_value
    net_sale_proceeds = final_home_value - selling_costs - remaining_mortgage
    discounted_proceeds = net_sale_proceeds / ((1 + investment_return) ** occupation_length)

    print(f"\nAt sale (year {occupation_length}):")
    print(f"Final home value: ${final_home_value:,.2f}")
    print(f"Selling costs: ${selling_costs:,.2f}")
    print(f"Remaining mortgage: ${remaining_mortgage:,.2f}")
    print(f"Net sale proceeds: ${net_sale_proceeds:,.2f}")
    print(f"Discounted proceeds: ${discounted_proceeds:,.2f}")

    npv_buy += discounted_proceeds
    return npv_buy


if __name__ == "__main__":
    args = parse_args()

    # Run the NPV calculation
    npv_buy = calculate_npv_buying(args.home_price, args.down_payment, args.mortgage_rate,
                                args.mortgage_term, args.occupation_length, args.appreciation_rate,
                                args.maintenance_cost_rate, args.tax_rate, args.closing_costs,
                                args.selling_cost_rate, args.investment_return)

    # Calculate renting NPV for comparison
    npv_rent = calculate_npv_renting(args.rent, args.occupation_length, args.investment_return)

    # Print statements with explanations for guessed values
    print(f"\nNPV of Buying: ${npv_buy:,.2f}")
    print(f"NPV of Renting: ${npv_rent:,.2f}")
    # Calculate monthly costs
    mortgage_payment = (args.home_price - args.down_payment) * (args.mortgage_rate / 12) / \
                      (1 - (1 + args.mortgage_rate / 12) ** (-args.mortgage_term * 12)) * 12
    maintenance = args.maintenance_cost_rate * args.home_price
    property_tax = args.tax_rate * args.home_price

    # Calculate stock market investment scenario
    # Assume down payment and monthly payment difference vs rent goes to stocks
    initial_stock_investment = args.down_payment + args.closing_costs
    monthly_payment_difference = (mortgage_payment / 12 + maintenance / 12 + property_tax / 12) - args.rent
    annual_stock_contribution = monthly_payment_difference * 12

    npv_stocks = calculate_stock_investment(initial_stock_investment,
                                          annual_stock_contribution,
                                          args.occupation_length,
                                          args.stock_market_return,
                                          args.investment_return)

    print(f"\nComparison of Options:")
    print(f"NPV of Buying: ${npv_buy:,.2f}")
    print(f"NPV of Renting: ${npv_rent:,.2f}")
    print(f"NPV of Renting + Stock Investment: ${(npv_rent + npv_stocks):,.2f}")
    print(f"Difference (Buying - Renting): ${(npv_buy - npv_rent):,.2f}")
    print(f"Difference (Buying - (Renting + Stocks)): ${(npv_buy - (npv_rent + npv_stocks)):,.2f}")
    print(f" - Home price: ${args.home_price:,} (Berkeley median value)")
    print(f" - Down payment: ${args.down_payment:,} (20% of home price)")
    print(f" - Mortgage rate: {args.mortgage_rate * 100:.2f}% (30-year fixed rate)")
    print(f" - Occupation length: {args.occupation_length} years (expected time before selling)")
    print(f" - Appreciation rate: {args.appreciation_rate * 100:.2f}% (long-term historical Berkeley average)")
    print(f" - Investment return rate: {args.investment_return * 100:.2f}% (expected moderate-risk portfolio return)")
    print(f" - Maintenance cost rate: {args.maintenance_cost_rate * 100:.2f}% (estimated higher for older homes)")
    print(f" - Property tax rate: {args.tax_rate * 100:.2f}% (California’s Prop 13 rate)")
    print(f" - Closing costs: ${args.closing_costs:.2f} (estimated at 3% of purchase price)")
    print(f" - Selling costs: {args.selling_cost_rate * 100:.2f}% (average agent fee plus other costs)")
