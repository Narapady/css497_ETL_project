from food_availability import FoodAvailablity
from nutrient_food_estimates import NutrientFoodEstimate
from fast_food import FastFood
from price_index import PriceIndex
from food_expenditure import FoodExpenditure


def main() -> None:
    # Process Food Availability 
    food = FoodAvailablity("Loss-Adjusted Food Availability")
    food.process_data()

    # Process nutrient intake and food consumption estimates
    nutrient_estimate = NutrientFoodEstimate("Nutrient Intake Estimates")
    food_estimate = NutrientFoodEstimate("Food Consumption Estimates")
    nutrient_estimate.process_data()
    food_estimate.process_data()

    # Process fast food purchasers
    dir_names = ["2014", "2015", "2016"]
    for directiory in dir_names:
       fastfood = FastFood(directiory)
       fastfood.process_data()
    
    # Process consumer price index and producer price index
    cpi = PriceIndex("Consumer Price Index", "consumer")
    ppi = PriceIndex("Producer Price Index", "producer")
    cpi.process_data()
    ppi.process_data()

    # Process food expenditure 
    food_exp = FoodExpenditure("Current Food Expenditure Series")
    food_exp.process_food_expenditure()
    food_exp.process_monthly_sale()
    

if __name__ == '__main__':
    main()
