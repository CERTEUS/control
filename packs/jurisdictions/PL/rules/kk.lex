# Minimal placeholder LEXLOG file for tests
DEFINE cel_korzysci_majatkowej
DEFINE wprowadzenie_w_blad
DEFINE niekorzystne_rozporzadzenie_mieniem

PREMISE P_CEL
PREMISE P_WPROWADZENIE
PREMISE P_ROZPORZADZENIE

RULE R_286_OSZUSTWO:
  IF P_CEL AND P_WPROWADZENIE AND P_ROZPORZADZENIE
  THEN K_OSZUSTWO_STWIERDZONE

CONCLUSION K_OSZUSTWO_STWIERDZONE ASSERT z3.And(cel_korzysci_majatkowej, wprowadzenie_w_blad)

