import time
import os
from Bio import SeqIO
import multiprocessing as mp
import numpy as np
import platform

import Util
import Logic
import LogicPrep
############### start to set env ################
SYSTEM_NM = platform.system()
if SYSTEM_NM == 'Linux':
    # REAL
    WORK_DIR = os.getcwd() + "/"
else:
    # DEV
    WORK_DIR = "D:/000_WORK/JangHyeWon/20201016/WORK_DIR/"
PROJECT_NAME = WORK_DIR.split("/")[-2]

INPUT = "input/"
OUTPUT = "output/"
# ANALYSIS_INFO = "!Substitution analysis_BE analyzer(L=30)_FAH.xlsx"
# ANALYSIS_INFO = "Substitution analysis_BE analyzer_201014 ngs.xlsx"  # 20201027 분석요청
ANALYSIS_INFO = "BE analyzer 분석_201014 ngs_FAH(R=10,n=1,L=30).xlsx"  # 20201118 분석요청

# trgt idx
LEN_TRGT_FRNT = 20
TRGT_IDX = [39, 40]  # if idx == 40 ==> [39, 40]
CONDITION_DICT = {
    'WT': [['A'], False, False]
    , 'intended_edit_at_trgt_pnt': [['G'], False, False]
    , 'intended_edit_with_indel': [['G'], False, True]
    , 'unintended_edit_at_trgt_pnt': [['C', 'T'], False, False]
    , 'unintended_edit_at_trgt_pnt_INDEL': [['C', 'T'], False, True]
    , 'intended_edit_at_trgt_pnt_other': [['G'], True, False]
    , 'intended_edit_at_trgt_pnt_other_INDEL': [['G'], True, True]
    , 'other_mod': [['A', 'C', 'T'], True, False]
    , 'other_mod_INDEL': [['A', 'C', 'T'], True, True]
}  # {opt_title: [[trgt_seq], sub_flag, indel_flag]}
LEN_TRGT_BACK = 20

INIT = [LEN_TRGT_FRNT, TRGT_IDX, LEN_TRGT_BACK]

TOTAL_CPU = mp.cpu_count()
MULTI_CNT = int(TOTAL_CPU*0.8)
############### end setting env #################

def main():
    util = Util.Utils()
    logic_prep = LogicPrep.LogicPreps()
    logic = Logic.Logics()

    sheet_names = util.get_sheet_names(WORK_DIR + INPUT + ANALYSIS_INFO)

    for sheet_name in sheet_names:
        df = util.read_excel_to_df(WORK_DIR + INPUT + ANALYSIS_INFO, sheet_name)
        df['Length'] = df['Length'].fillna(0.0)  # Length column is Count value
        df['Count'] = df['Count'].fillna(0.0)  # Length column is Count value

        result_dict = logic.analyze_mut(df, INIT, CONDITION_DICT)
        result_list = logic_prep.make_dict_to_list(result_dict)
        result_dict.clear()
        srted_result_list = logic_prep.sort_list_by_ele(result_list, 0, False)
        result_list.clear()

        header = ['condition', 'RGEN_treated_sequence', '', 'WT Sequence', 'count', 'subs_position_from_target']
        if len(result_list) > 1000000:
            util.make_tsv(WORK_DIR + OUTPUT + ANALYSIS_INFO.replace(".xlsx", "_" + sheet_name + "_rm_indel_idx"), header, srted_result_list)
        else:
            util.make_excel(WORK_DIR + OUTPUT + ANALYSIS_INFO.replace(".xlsx", "_" + sheet_name + "_rm_indel_idx"), header, srted_result_list)
        srted_result_list.clear()


if __name__ == '__main__':
    start_time = time.perf_counter()
    print("start [ " + PROJECT_NAME + " ]>>>>>>>>>>>>>>>>>>")
    main()
    print("::::::::::: %.2f seconds ::::::::::::::" % (time.perf_counter() - start_time))