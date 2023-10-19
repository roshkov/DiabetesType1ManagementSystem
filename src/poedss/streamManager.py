import logging
import pandas as pd
import os
import hashlib
from enum import Enum
import platform

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class ColumnNames(Enum):
    PATIENT = "patient"
    DATE = "date"
    TIME = "time"
    DATETIME = "datetime"
    GLUCOSE = "glucose"
    TYPE = "type"
    COMMENTS = "comments"


class StreamManager:

    glucose_df = None

    def __init__(self):
        self.glucose_df = pd.DataFrame(
            columns=[
                ColumnNames.PATIENT.value,
                ColumnNames.DATETIME.value,
                ColumnNames.GLUCOSE.value,
                ColumnNames.TYPE.value,
            ]
        )
        self.readFiles(self.getFiles())

    def getDataframe(self) -> pd.DataFrame:
        return self.glucose_df

    def appendDataframe(self, otherDataframe: pd.DataFrame) -> pd.DataFrame:
        self.glucose_df = pd.concat([self.glucose_df, otherDataframe])
        # Sort for good measure
        return self.sortDataframe()

    def readFiles(
        self, file_list: list[str], patient_dir_name: str = "patients"
    ) -> pd.DataFrame:
        if (platform.system() == "Windows"):
            patient_dir_loc = file_list[0].split("\\").index(patient_dir_name) + 1
        else:
            patient_dir_loc = file_list[0].split("/").index(patient_dir_name) + 1

        for path in file_list:
            temp_df = pd.read_csv(
                path,
                parse_dates={
                    ColumnNames.DATETIME.value: [
                        ColumnNames.DATE.value,
                        ColumnNames.TIME.value,
                    ]
                },
                usecols=[
                    ColumnNames.DATE.value,
                    ColumnNames.TIME.value,
                    ColumnNames.GLUCOSE.value,
                    ColumnNames.TYPE.value,
                    ColumnNames.COMMENTS.value,
                ],
            )
            patient = path.split("/")[patient_dir_loc].encode("utf-8")
            patient_id = self.makeHash(patient)
            temp_df[ColumnNames.PATIENT.value] = patient_id
            self.appendDataframe(temp_df)

    def getFiles(self, path: str = "./patients") -> list[str]:
        file_list = []
        for root, dirs, files in os.walk(path):
            print()
            for file in files:
                if file == "glucose.csv":
                    file_list.append(os.path.join(root, file))

        return file_list

    def makeHash(self, string: str) -> str:
        m = hashlib.md5()
        m.update(string)
        return m.hexdigest()[0:12]

    def sortDataframe(self) -> pd.DataFrame:
        self.glucose_df = self.glucose_df.sort_values(
            by=ColumnNames.DATETIME.value, ascending=True
        )
