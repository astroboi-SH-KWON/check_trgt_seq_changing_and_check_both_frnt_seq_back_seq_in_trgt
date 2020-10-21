import math
from astroboi_bio_tools.ToolLogic import ToolLogics

import LogicPrep
class Logics(ToolLogics):
    def check_mute_pos(self, mut_arr, needle_seq, fr_bc_flag=True, mut_checker='.'):
        for i in range(len(needle_seq)):
            if needle_seq[i] == mut_checker:
                if fr_bc_flag:
                    mut_arr.append(i - len(needle_seq))
                else:
                    mut_arr.append(i + 1)

        return mut_arr

    def analyze_mut(self, df, init, condi):
        logic_prep = LogicPrep.LogicPreps()
        result_dict = {}

        len_trgt_frnt = init[0]
        trgt_idx_st = init[1][0]
        trgt_idx_en = init[1][1]
        len_trgt_back = init[2]

        for ob in range(len(df)):
            needle_seq = df.loc[ob][1]
            rgen_seq = df.loc[ob][2]
            read_cnt = int(df.loc[ob][3])

            if isinstance(needle_seq, float):
                if math.isnan(needle_seq):
                    continue

            if isinstance(rgen_seq, float):
                if math.isnan(rgen_seq):
                    continue

            trgt_seq = rgen_seq[trgt_idx_st: trgt_idx_en]
            ned_frnt = logic_prep.get_target_seq(needle_seq, trgt_idx_st, len_trgt_frnt)
            ned_back = logic_prep.get_target_seq(needle_seq, trgt_idx_en, len_trgt_back, False)

            trgt_flag = False
            mut_arr = []
            if '.' in ned_frnt:
                trgt_flag = True
                self.check_mute_pos(mut_arr, ned_frnt)

            if '.' in ned_back:
                trgt_flag = True
                self.check_mute_pos(mut_arr, ned_back, False)

            for cndi_key, cndi_val in condi.items():
                cndi_seq_arr = cndi_val[0]
                mut_flag = cndi_val[1]

                for cndi_seq in cndi_seq_arr:
                    if trgt_seq == cndi_seq:
                        if trgt_flag == mut_flag:
                            seq_key = rgen_seq[trgt_idx_st - len_trgt_frnt: trgt_idx_en + len_trgt_back]
                            ned_seq = needle_seq[trgt_idx_st - len_trgt_frnt: trgt_idx_en + len_trgt_back]
                            if cndi_key in result_dict:
                                if seq_key in result_dict[cndi_key]:
                                    result_dict[cndi_key][seq_key][1] += read_cnt
                                else:
                                    tmp_arr = [ned_seq, read_cnt]
                                    tmp_arr.extend(mut_arr)
                                    result_dict[cndi_key].update({seq_key: tmp_arr})
                            else:
                                tmp_arr = [ned_seq, read_cnt]
                                tmp_arr.extend(mut_arr)
                                result_dict.update({cndi_key: {seq_key: tmp_arr}})

        return result_dict