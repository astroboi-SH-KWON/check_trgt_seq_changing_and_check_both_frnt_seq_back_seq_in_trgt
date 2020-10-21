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
ANALYSIS_INFO = "!Substitution analysis_BE analyzer(L=30)_FAH.xlsx"

# trgt idx
LEN_TRGT_FRNT = 20
TRGT_IDX = [39, 40]  # if idx == 40 ==> [39, 40]
CONDITION_DICT = {
    'WT': [['A'], False]
    , 'intended_edit_at_trgt_pnt': [['G'], False]
    , 'unintended_edit_at_trgt_pnt': [['C', 'T'], False]
    , 'intended_edit_at_trgt_pnt_other': [['G'], True]
    , 'other_mod': [['A', 'C', 'T'], True]
}  # False : no mute, True : mute
LEN_TRGT_BACK = 20

INIT = [LEN_TRGT_FRNT, TRGT_IDX, LEN_TRGT_BACK]

TOTAL_CPU = mp.cpu_count()
MULTI_CNT = int(TOTAL_CPU*0.8)
############### end setting env #################

def test():
    util = Util.Utils()
    logic_prep = LogicPrep.LogicPreps()
    logic = Logic.Logics()

    sheet_names = util.get_sheet_names(WORK_DIR + INPUT + ANALYSIS_INFO)

    df = util.read_excel_to_df(WORK_DIR + INPUT + ANALYSIS_INFO, sheet_names[0])

    len_trgt_frnt = INIT[0]
    trgt_idx_st = INIT[1][0]
    trgt_idx_en = INIT[1][1]
    len_trgt_back = INIT[2]

    result_dict = {}
    for ob in range(len(df)):
    # ob = 0
        needle_seq = df.loc[ob][1]
        rgen_seq = df.loc[ob][2]
        read_cnt = int(df.loc[ob][3])

        trgt_seq = rgen_seq[trgt_idx_st: trgt_idx_en]
        ned_frnt = logic_prep.get_target_seq(needle_seq, trgt_idx_st, len_trgt_frnt)
        ned_back = logic_prep.get_target_seq(needle_seq, trgt_idx_en, len_trgt_back, False)

        trgt_flag = False
        mut_arr = []
        if '.' in ned_frnt:
            trgt_flag = True
            logic.check_mute_pos(mut_arr, ned_frnt)

        if '.' in ned_back:
            trgt_flag = True
            logic.check_mute_pos(mut_arr, ned_back, False)

        for cndi_key, cndi_val in CONDITION_DICT.items():
            cndi_seq_arr = cndi_val[0]
            mut_flag = cndi_val[1]

            for cndi_seq in cndi_seq_arr:
                if trgt_seq == cndi_seq:
                    if trgt_flag == mut_flag:
                        seq_key = rgen_seq[trgt_idx_st - len_trgt_frnt: trgt_idx_en + len_trgt_back]
                        if cndi_key in result_dict:
                            if seq_key in result_dict[cndi_key]:
                                result_dict[cndi_key][seq_key][0] += read_cnt
                            else:
                                tmp_arr = [read_cnt]
                                tmp_arr.extend(mut_arr)
                                result_dict[cndi_key].update({seq_key: tmp_arr})
                        else:
                            tmp_arr = [read_cnt]
                            tmp_arr.extend(mut_arr)
                            result_dict.update({cndi_key: {seq_key: tmp_arr}})

    for cond, val_dict in result_dict.items():
        for seq_key, val in val_dict.items():
            if len(val) > 2:
                print(cond)
                print(seq_key)
                print(val)

if __name__ == '__main__':
    start_time = time.perf_counter()
    print("start [ " + PROJECT_NAME + " ]>>>>>>>>>>>>>>>>>>")
    test()
    print("::::::::::: %.2f seconds ::::::::::::::" % (time.perf_counter() - start_time))