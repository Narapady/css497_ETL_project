import pandas as pd
import os

class FoodExpenditure:
    new_dir = "food-expenditure-clean"
    os.mkdir(new_dir)
    
    def __init__(self, dirname: str):
        self.dirname = dirname 
    
    def process_food_expenditure(self) -> None:
        paths = [os.path.join(self.dirname, "constant_dollar_expenditures.xlsx"),
                 os.path.join(self.dirname, "nominal_expenditures.xlsx")]
        
        for path in paths:
            df = pd.read_excel(path)
            df.columns = df.iloc[3]
            df = df[4:29]
            year = df["Year"].tolist()
            result_dict = {col: i for i, col in enumerate(list(df.columns)) if "Total" in col} 
            df = df.drop("Year", axis=1)

            # breakpoint()
            start_pos = 0

            for key, end_pos in result_dict.items():
                new_df = df.iloc[:, start_pos:end_pos]
                new_df.insert(0, "year", year)
                
                prefix = path.split("/")[1].split("_")[0]
                filename = prefix + "-" + key.lower().replace(" ", "-")
                new_df.to_csv(f"{self.new_dir}/{filename}.csv", index=False)
                start_pos = end_pos + 1
                
    def process_monthly_sale(self) -> None:
        path = os.path.join(self.dirname, "monthly_sales.xlsx")
        df = pd.read_excel(path)
        
        df.columns = ["year", "month", "nominal_fah", "nominal_fafh", "total_nominal_sales","constant_fah", "constant_fafh", "total_constant_sales"]
        df = df[3:307]
        nominal_df = df.drop(["constant_fah", "constant_fafh", "total_constant_sales"], axis=1)
        constant_df = df.drop(["nominal_fah", "nominal_fafh", "total_nominal_sales"], axis=1)
        nominal_df.to_csv(f"{self.new_dir}/nominal-monthly-sale.csv", index=False)
        constant_df.to_csv(f"{self.new_dir}/constant-monthly-sale.csv", index=False)

# if __name__ == "__main__":
#     dirname = "Current Food Expenditure Series"
#     food_exp = FoodExpenditure(dirname)
#     food_exp.process_food_expenditure()
#     food_exp.process_monthly_sale()


