# check_trgt_seq_changing_and_check_both_frnt_seq_back_seq_in_trgt


	BE-analyzer align은 PAM 기준으로 60bp. 이후, code로 분석시에는 앞에 19bp는 제외시키고 edit base 기준으로 양쪽 20bp를 분석.											
												
	Condition											
a	Wild type	20bp-targeted point "A"-20bp 이 모두 ref와 같은 경우 (총 41bp의 seqeunce가 ref와 같은경우)										
b	Intended edit at the targeted point	targeted point가 "G"이면서, 양쪽으로 20bp (20bp-targeted point-20bp) 가 모두 ref와 같은경우										
c	Unintended edit at the targeted point	targeted point가 "C또는 T"이면서, 양쪽으로 20bp (20bp-targeted point-20bp) 가 모두 ref와 같은경우										
d	Intended edit at the targeted point, other modified	targeted point가 "G"이면서, 양쪽으로 20bp에 mutation이 있는 경우.										
e	other modified	targeted point가 "A또는 C또는 T"이면서, 양쪽으로 20bp에 mutation이 있는 경우. 										
f	Intended edit with indel	targeted point가 "G"이면서, insertion과 deletion이 41bp window내에 있는 경우										
g	indel	insertion/deletion만 41bp window내에 있는 경우										
