"""
lg2 handles the database work flow
data maped to cluster page and virtual page
"""

import os
import bson
import json
from datetime import datetime
from typing import Dict, TypeAlias, Union, List, Optional, Any
from ox_db.db.types import embd, uids

from ox_doc.ld import OxDoc
from ox_db.ai.vector import Model as vmd
from ox_db.ai.transfomer import Model as tmd
from ox_db.utils.dp import gen_uid, join_list, strorlist_to_list


class Oxdb:
    def __init__(self, db: str = "", db_path: Optional[str] = None):
        """
        Initialize instances of the Log class

        Args:
            db (str, optional): The name of the database. Defaults to "".
            db_path (Optional[str], optional): The path to the database directory. Defaults to None.
        """
        self.set_db(db, db_path)
        self.vec = vmd()
        self.tmd = tmd()

    def set_db(self, db: str, db_path: Optional[str] = None) -> str:
        """
        Sets the database path.

        Args:
            db (str): The database name.
            db_path (Optional[str]): The database path.

        Returns:
            str: The path to the database.
        """
        self.db = db
        self.db_path = (
            db_path
            if db_path
            else os.path.join(os.path.expanduser("~"), "ox-db", db + ".oxdb")
        )
        os.makedirs(self.db_path, exist_ok=True)
        return self.db_path

    def get_db(self) -> str:
        """
        Returns the current database path.

        Returns:
            str: The database path.
        """
        return self.db_path

    def get_record(self, record: Optional[str] = None):
        """
        get the Record instances

        Args:
            record (Optional[str], optional): The Record name. Defaults to None.

        Returns:
             The record instances.
        """
        self.record = Record(record)
        self.record.connect_db(self.db_path, self.vec, self.tmd)
        return self.record

    def get_records(self) -> list:
        """
        Returns the current Record.

        Returns:
            list: of all records
        """
        pass

    def info(self) -> dict:

        res = {
            "db": self.db,
            "db_path": self.db_path,
            "record_name": self.record.record_name,
            "record_path": self.record.record_path,
            "vec_model": self.vec.md_name,
        }
        return res


class Record:
    def __init__(self, record: Optional[str] = None):
        """db record handler"""
        self.record_name = record or "log-" + datetime.now().strftime("[%d-%m-%Y]")

    def connect_db(self, db_path, vec, tmd):
        self.db_path = db_path
        self.vec = vec
        self.tmd = tmd
        self.record_path = os.path.join(self.db_path, self.record_name)
        os.makedirs(self.record_path, exist_ok=True)
        self.record_index_path = os.path.join(
            self.record_path, self.record_name + ".index"
        )

        self.index_oxd = self.oxd_load("index.oxd")
        self.vpage_oxd = self.oxd_load("vpage.oxd")
        self.cpage_oxd = self.oxd_load("cpage.oxd")
        self.data_oxd = self.oxd_load("data.oxd")
        self.vec_oxd = self.oxd_load("vec.oxd")

        self.record_reg = {
            "record_name": self.record_name,
            "record_path": self.record_path,
            "vec_model": self.vec.md_name,
            "entry": 0,
            "current_vpageid": "vpage-" + datetime.now().strftime("%d-%m-%Y"),
            "current_cpageid": "cpage-" + gen_uid(),
            "vpage_count": 0,
            "cpage_count": 0,
        }
        self.record_reg = self.index_oxd.get("record_reg") or self.record_reg
        self.index_oxd.set("record_reg", self.record_reg)

    def oxd_load(self, oxd_doc_name):
        oxd_doc_path = os.path.join(self.record_path, oxd_doc_name)
        return OxDoc(oxd_doc_path)

    def info(self) -> dict:
        return self.record_reg

    def push(
        self,
        data: Any,
        key: Optional[str] = None,
        description: Optional[any] = None,
        metadata: Optional[Dict[str, Any]] = None,
        page: Optional[str] = None,
        vpageid: Optional[str] = None,
        embeddings: embd = True,
        **kwargs,
    ) -> str:
        """
        Pushes data to the log file. Can be called with either data or both key and data.

        Args:
            data (Any): The data to be logged.
            embeddings (bool, optional): Whether to generate embeddings. Defaults to True.
            description (Optional[any], optional): Description related to the data. Defaults to None.
            metadata (Optional[dict], optional): metadata related to the data. Defaults to None.
            key (Optional[str], optional): The key for the log entry. Defaults to None.
            data_type (Optional[str], optional): The data_type of log entry. Defaults to None.

        Returns:
            str: The unique ID of the log entry.
        """
        record = self.record_name
        data_uid = gen_uid()

        if data == "" or data is None:
            raise ValueError("ox-db : No data provided for logging")

        vpageid = page or vpageid
        vpageid = self.vpage_append(vpageid, data_uid)
        cpageid = self.cpage_append(data, data_uid)

        data_unit = {
            "uid": data_uid,
            "data": data,
            "key": key or "key",
            "description": description,
            "metadata": metadata,
            "page": page,
            "vpageid": vpageid,
            "cpageid": cpageid,
            "record": record,
            "time": datetime.now().strftime("%H:%M:%S"),
            "date": datetime.now().strftime("%d-%m-%Y"),
            "data_type": kwargs.get("data_type", type(data).__name__),
        }

        self.index_append(data_uid, data_unit)
        self.data_oxd.set(data_uid, data_unit)
        self.vec_append(self.vpage_oxd, vpageid)
        self.vec_append(self.cpage_oxd, cpageid)

        self.record_reg["current_vpageid"] = vpageid
        self.record_reg["current_vpageid"] = vpageid
        self.record_reg["entry"] += 1
        self.index_oxd.set("record_reg", self.record_reg)
        return data_uid

    def index_append(self, data_uid, data):
        date_hr = datetime.now().strftime("%d-%m-%Y_%H")
        self.oxd_append(self.index_oxd, data["date"], data_uid)
        self.oxd_append(self.index_oxd, date_hr, data_uid)
        self.oxd_append(self.index_oxd, data["key"], data_uid)
        self.oxd_append(self.index_oxd, data["record"], data_uid)

    def vec_append(self, page_oxd, pageid):
        page = page_oxd.get(pageid)
        data = []
        for uid in page["lines"]:
            dunit = self.data_oxd.get(uid)
            data.append(dunit["data"])
        page_line_datas = join_list(data)[0]
        vec_page_lines = self.vec.encode(page_line_datas)
        self.vec_oxd.set(pageid, vec_page_lines)
        return pageid

    def vpage_append(self, vpageid, data_uid):
        if vpageid == None:
            vpageid = "vpage-" + datetime.now().strftime("%d-%m-%Y")
        
        
        page_content = self.vpage_oxd.get(vpageid)

        if page_content == None:
       
            page_content = {
                "uid": vpageid,
                "lines": [data_uid],
            }
            self.vpage_oxd.set(vpageid, page_content)
            
        else:
            lines = page_content["lines"]
            lines.append(data_uid)
            page_content["lines"] = lines

            self.vpage_oxd.set(vpageid, page_content)
        status = self.oxd_append(self.vpage_oxd, "all_page", vpageid)
        if status:
            self.record_reg["vpage_count"] += 1
        return vpageid

    def cpage_append(self, data, data_uid):

        data_len = self.tmd.count_token(data)
        cpageid = self.relevent_cpage(data)
        page_content = self.cpage_oxd.get(cpageid)

        if page_content == None:
            full = True if data_len > self.tmd.max_tokens else False
            page_content = {
                "uid": cpageid,
                "lines": [data_uid],
                "full": full,
                "page_len": data_len,
            }
            self.cpage_oxd.set(cpageid, page_content)
            
        else:
            lines = page_content["lines"]
            lines.append(data_uid)
            page_content["lines"] = lines
            page_content["page_len"] += data_len
            page_content["full"] = (
                True if page_content["page_len"] > self.tmd.max_tokens else False
            )

            self.cpage_oxd.set(cpageid, page_content)
        status = self.oxd_append(self.cpage_oxd, "all_page", cpageid)
        if status:
             self.record_reg["cpage_count"] += 1
        return cpageid

    def relevent_cpage(self, data):
        all_page = self.cpage_oxd.get("all_page")
        cpageid = "cpage-" + gen_uid()
        if all_page:
            cpageids = []
            for d in all_page:
                cpage = self.cpage_oxd.get(d)
                if cpage["full"] != True:
                    cpageids.append(cpage["uid"])
            if len(cpageids) > 0:
                searchresuid = self.search(data, 1, uid=cpageids)
                cpageid = searchresuid[0] if len(searchresuid) > 0 else cpageid

        self.oxd_append(self.cpage_oxd, "all_page", cpageid)

        return cpageid

    def pull(
        self,
        uid: uids = None,
        key: Optional[str] = None,
        time: Optional[str] = None,
        date: Optional[str] = None,
        recordfile: Optional[str] = "data.oxd",
        where: Optional[dict] = None,
        where_data: Optional[dict] = None,
    ) -> List[dict]:
        """
        Retrieves log entries based on unique ID, key, time, or date.

        Args:
            uid (uids): The unique ID of the log entry. Defaults to None.
            key (Optional[str], optional): The key of the log entry. Defaults to None.
            time (Optional[str], optional): The time of the log entry. Defaults to None.
            date (Optional[str], optional): The date of the log entry. Defaults to None.
            recordfile (Optional[str], optional): The specific sub file within the Record. Defaults to None.
                eg : ["data.oxd","vec.oxd",".index"]
            where={"metadata_key": "value"},
            where_data={"in_data":"search_string"} ,

        Returns:
            List[dict]: The log entries matching the criteria.
        """
        if recordfile not in [
            "data.oxd",
            "vec.oxd",
            "index.oxd",
            "vpage.oxd",
            "cpage.oxd",
        ]:
            raise ValueError(
                f"""ox-db : recordfile should be ["data.oxd","vec.oxd",".index"] not {recordfile} """
            )

        all_none = all(var is None for var in [key, uid, time, date, where, where_data])

        log_entries = []
        if all_none:
            doc = self.oxd_load(recordfile)
            content = doc.load_data()
            for uidx, unit in content.items():
                log_entries.append(
                    {
                        "uid": uidx,
                        "unit": unit,
                    }
                )
            return log_entries

        if uid is not None:
            uids = strorlist_to_list(uid)
            return self.pull_oxd_by_uid(uids, recordfile)

        if any([key, time, date, where]):
            uids = self.search_uid(key, time, date, where)
            log_entries_data = self.pull(uid=uids, recordfile=recordfile)
            log_entries.extend(log_entries_data)
            return log_entries

    def pull_oxd_by_uid(self, uids, recordfile):
        log_entries = []
        oxd_doc = self.oxd_load(recordfile)
        for u in uids:
            unit = oxd_doc.get(u)
            if not unit:
                continue
            log_entries.append(
                {
                    "uid": u,
                    "unit": unit,
                }
            )
        return log_entries

    def search(
        self,
        query: str,
        topn: int = 10,
        log_entries: Optional[List[dict]] = None,
        by: Optional[str] = "dp",
        uid: uids = None,
        key: Optional[str] = None,
        time: Optional[str] = None,
        date: Optional[str] = None,
        where: Optional[dict] = None,
        where_data: Optional[dict] = None,
    ) -> List[str]:
        """
        Searches log entries based on a query and retrieves the top matching results.

        Args:
            query (str): The search query.
            topn (int, optional): Number of top results to return. Defaults to 10.
            uid (uids, optional): The unique ID(s) of the log entry. Defaults to None.
            key (Optional[str], optional): The key of the log entry. Defaults to None.
            time (Optional[str], optional): The time of the log entry. Defaults to None.
            date (Optional[str], optional): The date of the log entry. Defaults to None.
            where={"metadata_key": "value"},
            log_entries (Optional[List[dict]], optional): The log entry [{"uid":uid,unit:{"data":data,"description":description}}]  Defaults to None.
            by (Optional[str], optional): method of search
                dp : Dot Product (default)
                ed : Euclidean Distance
                cs : Cosine Similarity


        Returns:
            List[uid]: The uids of matching log entries
        """
        log_entries = log_entries or self.pull(
            uid, key, time, date, recordfile="vec.oxd", where=where
        )
 
        dataset = [entry["unit"] for entry in log_entries]
        top_idx = self.vec.search(query, dataset, topn=topn, by=by)
        if len(top_idx) == 0:
            return []
        
        uids = [log_entries[idx]["uid"] for idx in top_idx]
        # res_data = self.pull(uid=uids)

        return uids

    def show(
        self,
        key: Optional[str] = None,
        uid: uids = None,
        time: Optional[str] = None,
        record: Optional[str] = None,
        date: Optional[str] = None,
    ):
        # Placeholder for future implementation
        pass

    def embed_all(self, record: str):
        # Placeholder for future implementation
        pass

    @staticmethod
    def oxd_append(oxd_doc, key, data):
        val = oxd_doc.get(key)
        if val != None and type(val) == list:
            if not data in val:
                val.append(data)
                oxd_doc.set(key, val)
                return True
        elif val == None:
            oxd_doc.set(key, [data])
            return True
        else:
            raise ValueError("ox-db: give ox_doc type is not list")

        return False

    def oxd_change(ox_doc, key, data):
        pass

    def search_uid(
        self,
        key: Optional[str] = None,
        time: Optional[str] = None,
        date: Optional[str] = None,
        where: Optional[dict] = None,
    ) -> List[str]:
        """
        Searches for UIDs based on key, time, or date.

        Args:
            key (Optional[str], optional): The key to search. Defaults to None.
            time (Optional[str], optional): The time to search. Defaults to None.
            date (Optional[str], optional): The date to search. Defaults to None.

        Returns:
            List[str]: The matching UIDs.
        """
        # res = search_uid(self.record_index, key, time, date, where)
        return None
