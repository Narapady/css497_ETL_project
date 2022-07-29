import pandas as pd 
import os

class FastFood:
    new_dir = "fast-food-clean"
    os.mkdir(new_dir)
   
    def __init__(self, dirname: str):
        self.dirname = dirname 
    
    def get_path(self) -> str:
        if self.dirname == "2014":
            return os.path.join(self.dirname, f"table4_{self.dirname}.xls")
        
        return  os.path.join(self.dirname, f"Table4_{self.dirname}.xlsx")
            
    def process_data(self) -> None:
        
        df = pd.read_excel(self.get_path())
        
        if  self.dirname == "2016":
            df.columns = ["times/week", "unit", "total", "men", "women", "total_se", "men_se", "women_se"]
            end = df[df["times/week"] == "By age"].index[0] - 1
            df = df.iloc[3:end, :5]
        else:
            df.columns =["times/week", "unit", "total", "men", "women"] 
            end = df[df["times/week"] == "By age"].index[0] - 1
            df = df.iloc[3:end, :]

        df = df.dropna()
        age_group = ["age-15-and-older", "age-18-and-older"]
        middle = int(df.shape[0] / 2) + 1
        df1, df2 = df.iloc[:middle,:], df.iloc[middle: ,:]
        
        df1.to_csv(f"{self.new_dir}/{age_group[0]}-{self.dirname}.csv", index=False) 
        df2.to_csv(f"{self.new_dir}/{age_group[1]}-{self.dirname}.csv", index=False) 

if __name__ == "__main__":
    dir_names = ["2014", "2015", "2016"]
    for directiory in dir_names:
       fastfood = FastFood(directiory)
       fastfood.process_data()
