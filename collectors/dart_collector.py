import io
import json
import os
import zipfile
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()


class DartCollector:

    BASE_URL = "https://opendart.fss.or.kr/api"

    def __init__(self):
        self.api_key = os.getenv("API_KEY")

        if not self.api_key:
            raise ValueError("API_KEY가 존재하지 않습니다.")

        self.corp_codes = None

    # ==========================================================
    # Corp Code
    # ==========================================================

    def load_corp_codes(self):

        url = f"{self.BASE_URL}/corpCode.xml"

        response = requests.get(
            url,
            params={"crtfc_key": self.api_key},
            timeout=30,
        )
        response.raise_for_status()

        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            with z.open(z.namelist()[0]) as xml:
                df = pd.read_xml(xml)

        df["corp_code"] = df["corp_code"].astype(str).str.zfill(8)
        df["stock_code"] = (
            df["stock_code"]
            .fillna("")
            .astype(str)
            .str.zfill(6)
        )

        self.corp_codes = df

        return df

    def get_corp_code(self, company_name: str) -> str:

        if self.corp_codes is None:
            self.load_corp_codes()

        result = self.corp_codes[
            self.corp_codes["corp_name"] == company_name
        ]

        if result.empty:
            raise ValueError(f"'{company_name}' 기업을 찾을 수 없습니다.")

        return result.iloc[0]["corp_code"]

    # ==========================================================
    # 공시목록
    # ==========================================================

    def get_disclosure_list(
        self,
        corp_code,
        bgn_de,
        end_de,
        all_pages=True,
    ):

        url = f"{self.BASE_URL}/list.json"

        all_list = []
        meta = None
        page_no = 1

        while True:

            response = requests.get(
                url,
                params={
                    "crtfc_key": self.api_key,
                    "corp_code": corp_code,
                    "bgn_de": bgn_de,
                    "end_de": end_de,
                    "page_no": page_no,
                    "page_count": 100,
                },
                timeout=30,
            )

            response.raise_for_status()

            data = response.json()

            if data["status"] != "000":
                raise Exception(data["message"])

            if meta is None:
                meta = {
                    "status": data["status"],
                    "message": data["message"],
                    "total_count": data["total_count"],
                    "total_page": data["total_page"],
                }

            all_list.extend(data.get("list", []))

            if not all_pages:
                break

            if page_no >= data["total_page"]:
                break

            page_no += 1

        meta["list"] = all_list

        return meta

    # ==========================================================
    # JSON → DataFrame
    # ==========================================================

    @staticmethod
    def to_dataframe(disclosure_json):

        return pd.DataFrame(disclosure_json["list"])

    # ==========================================================
    # 보고서 필터
    # ==========================================================

    @staticmethod
    def filter_reports(
        disclosure_df,
        keywords=None,
    ):

        if keywords is None:
            keywords = [
                "사업보고서",
                "반기보고서",
                "분기보고서",
            ]

        mask = disclosure_df["report_nm"].apply(
            lambda x: any(keyword in x for keyword in keywords)
        )

        return disclosure_df.loc[mask].reset_index(drop=True)

    # ==========================================================
    # JSON 저장
    # ==========================================================

    @staticmethod
    def save_json(data, path):

        path = Path(path)

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(path, "w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                ensure_ascii=False,
                indent=4,
            )