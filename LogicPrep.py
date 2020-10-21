
from astroboi_bio_tools.ToolLogicPrep import ToolLogicPreps
class LogicPreps(ToolLogicPreps):
    def get_target_seq(self, full_seq, trgt_idx, len_trgt, flag=True):
        if flag:
            return full_seq[trgt_idx - len_trgt: trgt_idx]
        else:
            return full_seq[trgt_idx: trgt_idx + len_trgt]

    def make_dict_to_list(self, data_dict):
        result_list = []
        for condi, val_dict in data_dict.items():
            for rgen_seq, val_arr in val_dict.items():
                result_list.append([condi, rgen_seq] + val_arr)

        return result_list
