import pandas as pd
import os
import numpy as np

def get_paths(dirname: str) -> list[str]:
    all_files = os.listdir(dirname)
    return [f"{dirname}/{filename}" for filename in all_files]

def has_numbers(input_str: str) -> bool:
    if input_str.startswith("19") or input_str.startswith("20"):
        return True
    return False

class FoodAvailablity:

    def __init__(self, dirname: str):
        self.dirname = dirname 
        self.new_dir = self.dirname.lower().replace(" ", "-") + "-clean"
        os.mkdir(self.new_dir)

    def process_data(self) -> None:
        self.process_calories()
        self.process_foodgroups()
        
    def process_calories(self) -> None:
        """
        Process and clean calories.xls. The resulting dataframes are:
            - totals.csv: average daily per capita total calories from U.S food availability after loss adjusted
            - percents.csv: average daily per capita total calories percentage from U.S food availability after loss adjusted
        """
        filename = "calories.xls"
        path = os.path.join(self.dirname, filename)
        
        for sheet in range(1,3):
            df = pd.read_excel(path, sheet_name=sheet)
            sheetnames = pd.ExcelFile(path).sheet_names 
            df.columns = df.iloc[0]
            
            if sheet == 1:
                last_index = df[df['Year'] == 2017].index[0] + 1
            elif sheet == 2:
                last_index = df[df['Year'] == 2010].index[0] + 1
                
            df = df[4: last_index]
            df.reset_index(drop=True, inplace=True)
            index = df.loc[df["Year"] == "2000*"].index[0]
            df.loc[index:index+1,"Year"] = "2000"

            df.to_csv(f"{self.new_dir}/{sheetnames[sheet].lower()}.csv", index=False)

    def process_foodgroups(self) -> None:
        """
        Process and clean food groups in Loss-Adjusted-Food-Availability.
        For each food group, the function process each sheet and create new
        dataframes as separate files in corresponding directory.
        Food group include:
            - dairy
            - fat
            - fruit
            - grains
            - meat
            - sugar
            - veggie
        """
        
        file_paths = get_paths(self.dirname)
        for path in file_paths:
            if "calories" in path or "serving" in path:
                continue
            # get sheets to process
            file = pd.ExcelFile(path)
            sheet_names = file.sheet_names[1:]
            
            sub_dir = path[path.rfind("/") + 1: path.rfind(".")].lower()
            dir_path = os.path.join(self.new_dir, sub_dir)

            try:
                os.mkdir(dir_path)
            except OSError as e:
                print(e)

            # each sheet
            for name in sheet_names:
                # read each sheet in the file
                print(f"- {name}")
                df = pd.read_excel(path, sheet_name=name)
                # use title as key 
                # title is header of each sheet
                filename = df.columns[0].split(":")[0].lower()
                filename = filename.replace(" ", "-").replace("/", "-")

                df.columns = df.iloc[0]
                filters = df['Year'].apply(lambda x: has_numbers(str(x)))
                df = df[filters]               
                
                df.columns = self.change_nan_cols(df)
                new_col_names = self.change_col_names(df)
                df = df.rename(columns=new_col_names)
                final_cols = ["year", "original weight", "edible weight", "total percent loss", "loss lbs/year", "loss g/day", "available calories/day"]
                
                # total grains has no edible weight column 
                if name == 'Total grains':
                    final_cols.remove("edible weight")
                df = df[final_cols]
                print(f"{dir_path}/{filename}.csv")
                df.to_csv(f"{dir_path}/{filename}.csv", index=False)         
    
    def change_nan_cols(self, df: pd.DataFrame) -> list[str]:
        """
        Helper function that handle nan columns.
        """
        cols = list(df.columns)
        indx = [i for i, col in enumerate(cols) if col is np.nan]

        if len(indx) == 2:
            new_cols = ["Loss oz/day", "Loss g/day"]
        elif len(indx) == 3:
            new_cols = ["Loss gal/year", "Loss oz/day", "Loss g/day"]
        elif len(indx) == 4:
            new_cols = ["Edible weight", "Other loss", "Loss oz/day", "Loss g/day"]
        elif len(indx) == 5:
            new_cols = ["Edible weight", "Other loss", "Loss gal/year", "Loss oz/day", "Loss g/day"]
        for i, col in zip(indx, new_cols):
            cols[i] = col
            
        return cols

    def change_col_names(self, df: pd.DataFrame) -> dict[str, str]:
        """
        Helper function that rename columns name of food group availability
        """
        avail_cal = ""
        primary_weight = ""
        for col in list(df.columns):
            if str(col).startswith("Calories"):
                avail_cal = col 
        for col in list(df.columns):
            if str(col).startswith("Primary"):
                primary_weight = col 
                
        new_col_names = {
            "Year": "year",
            primary_weight: "original weight",
            "Edible weight": "edible weight",
            "Total loss, all levels": "total percent loss",
            "Per capita availability adjusted for loss": "loss lbs/year",
            "Loss g/day": "loss g/day",
            avail_cal: "available calories/day"
            
        }
        
        return new_col_names

if __name__ == "__main__":
    directory_name = "Loss-Adjusted Food Availability"
    food = FoodAvailablity(directory_name)
    food.process_data()
