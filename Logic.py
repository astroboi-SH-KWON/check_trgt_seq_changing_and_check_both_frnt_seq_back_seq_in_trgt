import math
from astroboi_bio_tools.ToolLogic import ToolLogics

import LogicPrep
class Logics(ToolLogics):
    def check_subs_pos(self, mut_arr, needle_seq, fr_bc_flag=True, subs_checker='.'):
        for i in range(len(needle_seq)):
            if needle_seq[i] == subs_checker:
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
            wt_seq = df.loc[ob][0]
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
            subs_arr = []
            if '.' in ned_frnt:
                trgt_flag = True
                self.check_subs_pos(subs_arr, ned_frnt)

            if '.' in ned_back:
                trgt_flag = True
                self.check_subs_pos(subs_arr, ned_back, False)

            for cndi_key, cndi_val in condi.items():
                cndi_seq_arr = cndi_val[0]
                subs_flag = cndi_val[1]
                indel_flag = cndi_val[2]

                for cndi_seq in cndi_seq_arr:
                    if trgt_seq == cndi_seq:
                        if trgt_flag == subs_flag:
                            seq_key = rgen_seq[trgt_idx_st - len_trgt_frnt: trgt_idx_en + len_trgt_back]
                            sliced_wt_seq = wt_seq[trgt_idx_st - len_trgt_frnt: trgt_idx_en + len_trgt_back]
                            ned_seq = needle_seq[trgt_idx_st - len_trgt_frnt: trgt_idx_en + len_trgt_back]

                            if self.is_indel(seq_key) and indel_flag:
                                self.add_to_dict(result_dict, subs_arr, cndi_key, seq_key, ned_seq, sliced_wt_seq, read_cnt)

                            elif self.is_indel(seq_key) == False and indel_flag == False:
                                self.add_to_dict(result_dict, subs_arr, cndi_key, seq_key, ned_seq, sliced_wt_seq, read_cnt)

        return result_dict

    def is_indel(self, trgt_seq, indel_checker='-'):
        if indel_checker in trgt_seq:
            return True
        return False

    def add_to_dict(self, result_dict, subs_arr, cndi_key, seq_key, ned_seq, sliced_wt_seq, read_cnt):
        if cndi_key in result_dict:
            if seq_key in result_dict[cndi_key]:
                result_dict[cndi_key][seq_key][2] += read_cnt
            else:
                tmp_arr = [ned_seq, sliced_wt_seq, read_cnt]
                tmp_arr.extend(subs_arr)
                result_dict[cndi_key].update({seq_key: tmp_arr})
        else:
            tmp_arr = [ned_seq, sliced_wt_seq, read_cnt]
            tmp_arr.extend(subs_arr)
            result_dict.update({cndi_key: {seq_key: tmp_arr}})