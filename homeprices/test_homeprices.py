import unittest
from homeprices import (
    calculate_npv_buying, 
    calculate_npv_renting,
    calculate_stock_investment
)

class TestHomePrices(unittest.TestCase):
    def setUp(self):
        # Common test parameters
        self.home_price = 1_000_000
        self.down_payment = 200_000
        self.mortgage_rate = 0.065
        self.mortgage_term = 30
        self.appreciation_rate = 0.056
        self.maintenance_cost_rate = 0.015
        self.tax_rate = 0.0079
        self.closing_costs = 30_000
        self.selling_cost_rate = 0.06

    def test_zero_year_occupancy(self):
        """Test that NPV is negative for immediate sale due to transaction costs"""
        npv = calculate_npv_buying(
            self.home_price,
            self.down_payment,
            self.mortgage_rate,
            self.mortgage_term,
            occupation_length=0,
            appreciation_rate=self.appreciation_rate,
            maintenance_cost_rate=self.maintenance_cost_rate,
            tax_rate=self.tax_rate,
            closing_costs=self.closing_costs,
            selling_cost_rate=self.selling_cost_rate
        )
        self.assertLess(npv, 0, "NPV should be negative for immediate sale due to transaction costs")

    def test_one_year_occupancy(self):
        """Test one year occupancy with typical parameters"""
        npv = calculate_npv_buying(
            self.home_price,
            self.down_payment,
            self.mortgage_rate,
            self.mortgage_term,
            occupation_length=1,
            appreciation_rate=self.appreciation_rate,
            maintenance_cost_rate=self.maintenance_cost_rate,
            tax_rate=self.tax_rate,
            closing_costs=self.closing_costs,
            selling_cost_rate=self.selling_cost_rate
        )
        # NPV should be defined (not None)
        self.assertIsNotNone(npv)

    def test_npv_renting(self):
        """Test that NPV of renting calculation works as expected"""
        monthly_rent = 2600
        occupation_length = 5
        npv = calculate_npv_renting(monthly_rent, occupation_length)
        self.assertIsNotNone(npv)
        self.assertLess(npv, 0, "NPV of renting should be negative (outflows)")
        
    def test_stock_investment(self):
        """Test that stock market investment calculation works as expected"""
        initial_investment = 100_000
        annual_contribution = 12_000
        years = 5
        return_rate = 0.06
        
        npv = calculate_stock_investment(initial_investment, annual_contribution, years, return_rate)
        self.assertIsNotNone(npv)
        # With positive return rate and contributions, final NPV should be positive
        self.assertGreater(npv, 0)

    def test_no_appreciation(self):
        """Test scenario with zero appreciation rate"""
        npv = calculate_npv_buying(
            self.home_price,
            self.down_payment,
            self.mortgage_rate,
            self.mortgage_term,
            occupation_length=5,
            appreciation_rate=0.0,
            maintenance_cost_rate=self.maintenance_cost_rate,
            tax_rate=self.tax_rate,
            closing_costs=self.closing_costs,
            selling_cost_rate=self.selling_cost_rate
        )
        # NPV should be negative with no appreciation due to costs
        self.assertLess(npv, 0)

if __name__ == '__main__':
    unittest.main()
