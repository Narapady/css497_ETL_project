import pandas as pd
import numpy as np
import os

class PriceIndex:
    new_dir = "price-index-clean"
    os.mkdir(new_dir)
    
    def __init__(self, dirname: str, pi_type: str):
        self.dirname = dirname 
        self.pi_type = pi_type 
    
    def get_2022_pct_change(self,path: str) -> list[float]:
        df = pd.read_excel(path)
        if self.pi_type == "consumer":
            col = "Forecast range2 2022"
        elif self.pi_type == "producer":
            col = "Forecast range1 2022"
        
        df.columns = df.iloc[0]
        df = df[2:].dropna(how="all")
        pct_change = df[col].tolist()[:-5]
        result = []
        for pct in pct_change:
            if pct is np.nan:
                result.append(np.nan)
            elif "to" in pct:
                num = pct.split("to")
                num1, num2 = float(num[0].strip()[:3]), float(num[1].strip()[:3]) 
                result.append(np.mean([num1, num2]))        

        return result  

    def get_path(self) -> str:
        if self.dirname == "Consumer Price Index":
            filename = "historicalcpi.xlsx"
        elif self.dirname == "Producer Price Index":
            filename = "historicalppi.xlsx" 
            
        return os.path.join(self.dirname,filename)

    def process_data(self) -> None:

        df = pd.read_excel(self.get_path())
        df.columns = df.iloc[0]
        
        if self.pi_type == "consumer":
            df = df.iloc[1:27, :list(df.columns).index(2021.0) + 1].dropna(how="all")
            pct_change_2022_path = "./Consumer Price Index/CPIforecast.xlsx"
            
        elif self.pi_type == "producer":
            df = df.iloc[1:26, :list(df.columns).index(2021.0) + 1].dropna(how="all")
            pct_change_2022_path = "./Producer Price Index/PPIforecast.xlsx"
            
        cols = [str(year) for year in list(df.columns)]
        cols[1:] = [year[:-2] for year in cols[1:]]
        df.columns = cols

        df.insert(df.shape[1], "2022", self.get_2022_pct_change(pct_change_2022_path))
        df.reset_index(drop=True, inplace=True)
        
        df.to_csv(f"{self.new_dir}/{self.pi_type}-price-index.csv", index=False)

if __name__ == "__main__":
        
    cpi_dir = "Consumer Price Index"
    ppi_dir = "Producer Price Index"
   
    cpi = PriceIndex(cpi_dir, "consumer")
    ppi = PriceIndex(ppi_dir, "producer")

    cpi.process_data()
    ppi.process_data()
