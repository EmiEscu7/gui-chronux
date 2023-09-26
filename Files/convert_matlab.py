import pandas as pd
import scipy

class ConvertMatlab:
    _instance = None
    _matlab_file = './Convert/'
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ConvertMatlab, cls).__new__(cls)

        return cls._instance

    def csv_to_matlab(self, path, name):
        # Read the CSV file into a Pandas DataFrame.
        df = pd.read_csv(path)

        # Convert the DataFrame to a MATLAB dictionary.
        # nexColumnNames = []
        # nex = pd.DataFrame()
        # for col in df.columns:
        #     nexColumnNames.append(col.strip())
        #     nex.append(df[col].to_numpy().transpose())

        mat_dict = {
            'nexColumnNames': df.columns.to_numpy().transpose(),
            'nex': df.values
        }

        # Save the MATLAB dictionary to a MATLAB file.
        scipy.io.savemat(f'{self._matlab_file}{name}.mat', mat_dict)
