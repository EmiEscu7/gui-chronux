from Exports.export import Export
from Utils.alert import Alert
from Utils.loading import Loading
import pandas as pd


class ExcelExport(Export):

    def __init__(self):
        super().__init__()

    def export(self, columns, data, file_name = 'analysis') -> None:
        try:
            df = pd.DataFrame(list(zip(*data)), columns=columns)
            print(f"Export excel in {file_name} ...")
            with pd.ExcelWriter(f"{file_name}.xlsx") as writer:
                df.to_excel(writer)
            Alert(title='Export', message=f'Excel file generated in the route: {file_name}.xlsx').show()
        except:
            Alert(title='Error', message=f'An error occurred when exporting information to excel file.').show()
            Loading().change_state()
