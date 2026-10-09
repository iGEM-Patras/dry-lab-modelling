# Παραδοτέα Dry Lab: engineered PENK (iGEM Patras)

**Για:** ομάδα wet lab
**Ημερομηνία:** 2026-09-07
**Κατάσταση:** όλα τα παρακάτω είναι υπολογιστικά αποτελέσματα (dry lab). Τίποτα δεν έχει
μετρηθεί στο εργαστήριο. Οι αγγλικοί τεχνικοί όροι διατηρούνται όπως είναι, ώστε να ταιριάζουν
με τα σωληνάκια, το order sheet και τη βιβλιογραφία.

---

## 0. Το βασικό μήνυμα: τα 7 cassettes ΔΕΝ είναι χαλασμένα

Κάποια ανάλυση σας είπε ότι τα 7 cassettes δεν λειτουργούν. **Αυτό είναι λάθος**, και ο λόγος
είναι συγκεκριμένος: η ανάλυση εφάρμοσε το κριτήριο *«είναι αυτό native PENK;»*. Η απάντηση
είναι όχι: **σκόπιμα**. Αυτό είναι όλο το project.

Το κατασκεύασμα δεν είναι κατεστραμμένο PENK. Είναι **χίμαιρα δύο φυσικών οπιοειδών πεπτιδίων**:

- Το **message** κομμάτι `YGGF` διατηρείται ακέραιο από το ανθρώπινο PENK.
- Το **address** κομμάτι `EVVG` προέρχεται από τη **δελτορφίνη II**, φυσικό πεπτίδιο δέρματος
  βατράχου με εκλεκτικότητα για τον δ-υποδοχέα.

Δηλαδή αντικαθιστούμε **και** τη Met **και** τη Leu (native: 6× `YGGFM` + 1× `YGGFL`) με
7× `YGGFEVVG`. Το ώριμο πεπτίδιο είναι **οκταπεπτίδιο (8 aa)**, όχι πενταπεπτίδιο.

### Γιατί δύο cassettes «φαίνονται» προβληματικά

Επαληθεύτηκε απευθείας από το `engPENK_insert_annotated.gb` (μετάφραση του CDS, καταγραφή
κάθε flank):

| Cassette | θέση (aa) | upstream | downstream | Ετυμηγορία |
|---|---|---|---|---|
| 1 | 100 | KR | **KR**Y | dibasic: καθαρό οκταπεπτίδιο |
| 2 | 110 | KR | **KK**M | dibasic: καθαρό οκταπεπτίδιο |
| 3 | 142 | KR | **KK**D | dibasic, καθαρό οκταπεπτίδιο |
| 4 | 195 | KR | RGL | monobasic, **extended, εκ σχεδιασμού** |
| 5 | 222 | KR | **RR**V | dibasic, αλλά **κλάδος adrenorphin**, δίνει extended, όχι οκταπεπτίδιο |
| 6 | 245 | KR | **KR**F | dibasic, καθαρό οκταπεπτίδιο |
| 7 | 279 | KR | RF* | monobasic, **extended, εκ σχεδιασμού** |

Και τα 7 έχουν **ακέραιο upstream KR**. Τα cassettes 4 και 7 έχουν monobasic downstream, και
αυτές είναι **ακριβώς** οι θέσεις όπου το φυσικό PENK παράγει σκόπιμα *εκτεταμένα* πεπτίδια:
το οκταπεπτίδιο `YGGFMRGL` (MERGL) και το επταπεπτίδιο `YGGFMRF` (MERF). Το κατασκεύασμα
**αναπαράγει τη native αρχιτεκτονική**, δεν αποτυγχάνει να κοπεί.

> **Το αναμενόμενο αποτέλεσμα είναι: 4 καθαρά οκταπεπτίδια (`YGGFEVVG`, cassettes 1,2,3,6)
> + 3 extended species (cassettes 4, 5, 7).**
> ΟΧΙ 7 ταυτόσημα πεπτίδια. Αν δείτε αυτό το μοτίβο, είναι **επιτυχία**, όχι μερική αποτυχία.

Ο λόγος που το cassette 5 δίνει extended, παρότι έχει dibasic downstream (`RRV`): στο φυσικό
PENK ο πυρήνας 5 δεν απελευθερώνει πενταπεπτίδιο, μπαίνει στην οδό
**BAM-22 → BAM-20 → adrenorphin** (`YGGFMRRV`-NH₂). Το engineered cassette 5 ακολουθεί την ίδια
οδό. Δείτε §3 για τις 4 μάζες που προκύπτουν.

*Επίσημη καταγραφή: ο ισχυρισμός «τα cassettes 4 και 7 δεν θα δώσουν καθαρό προϊόν» έχει
ανακληθεί από το ίδιο το dry lab στο `NATIVE_PENK_AMENDMENT2_WETLAB.md` §0.2.*

---

## 1. Παραδοτέο: 4 πλασμίδια, έτοιμα για σύνθεση

| Construct | bp | GC πριν | GC μετά | CAI πριν | CAI μετά | Απώλεια CAI |
|---|---|---|---|---|---|---|
| mEGFP-P2A-His-PENK | 1674 | 57.5% | 40.0% | 0.863 | 0.736 | −14.7% |
| His-PENK-P2A-mEGFP | 1671 | 51.6% | 40.0% | 0.767 | 0.733 | −4.4% |
| mEGFP-IRES-His-PENK | 2197 | 58.6% | 45.0% | 0.753 | 0.694 | −7.8% |
| His-PENK-IRES-mEGFP |, | 58.6% | 45.0% | 0.709 | 0.651 | −8.2% |

**Επαληθεύτηκε σε όλα τα 4:** η πρωτεΐνη είναι **ταυτόσημη** σε κάθε cistron (καμία αλλαγή
αμινοξέος), **7 αντίγραφα** `YGGFEVVG` παρόντα, **signal peptide άθικτο**, **Kozak άθικτο**,
μηδέν νέα homopolymers ≥6, μηδέν ARE (`ATTTA`), μηδέν κρυφά polyA (`AATAAA`).

**Το κόστος, ειλικρινά:** το CAI πέφτει. Αυτό είναι πραγματικό trade-off για να φτάσουμε στο
GC window της σύνθεσης, δεν το κρύβουμε.

**Γιατί υπάρχουν και P2A και IRES εκδοχές:** το P2A αφήνει ένα υπόλειμμα ~21 aa στο
N-άκρο του δεύτερου πεπτιδίου, και η junction αυτή είναι το πιο ισχυρό immunogenicity hotspot
σε όλο το κατασκεύασμα, **όχι** το engineered επίτοπο. Το ζεύγος IRES είναι η εναλλακτική
χωρίς αυτό το υπόλειμμα.

---

## 2. Παραδοτέο: το HEK293T δεν μπορεί να κάνει τη δουλειά μόνο του

Αυτό είναι το **πιο σημαντικό** εύρημα για τον σχεδιασμό του πειράματος.

| Ένζυμο | Ρόλος | HEK293 nTPM | Παρόν; |
|---|---|---|---|
| **PCSK1** (PC1/3) | κοπή σε dibasic sites | 0.1 | **ΟΧΙ** |
| **PCSK2** (PC2) | κύριος παραγωγός μικρών οπιοειδών | 0.1 | **ΟΧΙ** |
| **SCG5** (7B2) | υποχρεωτικός chaperone του PC2 | 0.0 | **ΟΧΙ** |
| CPE | trimming C-terminal K/R | 73.7 | ναι |
| PAM | α-amidation | 37.5 | ναι |
| FURIN | constitutive convertase | 33.0 | ναι |
| CTSL (cathepsin L) | εναλλακτική οδός | 35.5 | ναι |
| PCSK1N (proSAAS) | **αναστολέας** του PC1/3 | 55.3 | ναι |

**Συνέπεια:** στο HEK293T το engPENK θα συσσωρευτεί ως **ανεπεξέργαστο precursor**. Δεν θα
σχηματιστούν μικρά οπιοειδή πεπτίδια. Και όχι μόνο λείπουν τα ένζυμα, υπάρχει και ο
**αναστολέας** proSAAS σε υψηλό επίπεδο.

**Άρα:** το «Stage 2» (προσθήκη recombinant convertases in vitro) **δεν είναι επιβεβαιωτικό
βήμα, είναι ολόκληρο το πείραμα.** Αν το παραλείψετε, δεν υπάρχει πείραμα.

**Δύο ακόμη συνέπειες που αλλάζουν το πρωτόκολλο:**
1. Το **siRNA knockdown** των πεπτιδασών δεν είναι δοκιμάσιμο εδώ: MME 0.7 και ANPEP 0.1 nTPM
   **απουσιάζουν ήδη**. Δεν υπάρχει τίποτα να γίνει knockdown· ένα null αποτέλεσμα δεν λέει τίποτα.
2. Στο plasmid 3 το mEGFP είναι **IRES-driven**, οπότε υπο-εκτιμά συστηματικά το PENK
   (IRES δεύτερο γονίδιο: 6–100% του cap-dependent, τυπικά 20–50%). Μην το χρησιμοποιήσετε ως
   ποσοτικό δείκτη του PENK.

**Καλό νέο, ειδικά για το HEK293T:** το PENK είναι 0.0 nTPM: δηλαδή **δεν υπάρχει ενδογενές
PENK background** σε αυτή τη σειρά. Η γενική προειδοποίηση του Amendment 2 («κάθε κυτταρική σειρά
με ακέραιο PENK locus εκκρίνει όλα αυτά πριν κάνετε transfection») ισχύει γενικά, αλλά το
HEK293T είναι η ευνοϊκή εξαίρεση. Τα untransfected controls παραμένουν **υποχρεωτικά**, αλλά
πιθανότατα θα είναι καθαρά.

---

## 3. Παραδοτέο: MS target list, τι να ψάξετε

| Species | Sequence | C-term | [M+H]⁺ | Από |
|---|---|---|---|---|
| Engineered mature | `YGGFEVVG` | free acid | **827.39** | cassettes 1,2,3,6 (τα 4 «καθαρά») |
| Engineered amidated | `YGGFEVV`-NH₂ | amide | 769.39 | μετά από PAM |
| Engineered extended | `YGGFEVVGRGL` | free acid | **1153.60** | cassette 4 (RGL) |
| Engineered extended | `YGGFEVVGRF` | free acid | **1130.56** | cassette 7 (RF) |
| Native MERGL | `YGGFMRGL` | free acid | 900.44 | native core 4 |
| Native MERF | `YGGFMRF` | free acid | 877.40 | native core 7 |

### Νέο εύρημα: 4 species που ΕΛΕΙΠΑΝ από τη λίστα

Το cassette 5 έχει downstream `RRVG`, που στο φυσικό PENK είναι ο κλάδος
**adrenorphin/metorphamide** και πιο κάτω τα BAM-20 / BAM-22. Η λίστα είχε τα **native** είδη
εκεί, αλλά **κανένα** από τα engineered αντίστοιχα:

| Engineered species | Sequence | [M+H]⁺ | Native αντίστοιχο |
|---|---|---|---|
| adrenorphin counterpart | `YGGFEVVGRRV`-NH₂ | **1237.68** | `YGGFMRRV`-NH₂ (984.52) |
| pre-PAM intermediate | `YGGFEVVGRRVG` | 1295.69 | `YGGFMRRVG` |
| BAM-20 counterpart | `YGGFEVVGRRVGRPEWWMDYQKR` | 2871.43 | BAM-20 (2618.27) |
| BAM-22 counterpart | `YGGFEVVGRRVGRPEWWMDYQKRYG` | 3091.51 | BAM-22 (2838.35) |

**Γιατί έχει σημασία:** αν το cassette 5 ακολουθήσει τον κλάδο adrenorphin και κανείς δεν κοιτάει
αυτά τα m/z, το προϊόν του είναι **αόρατο**. Θα αναφέρατε «μόνο 4 από 7 cassettes έδωσαν προϊόν»
ενώ στην πραγματικότητα έδωσαν 5 και ένα δεν παρακολουθήθηκε.

**⚠ Προσοχή σε σύγκρουση μαζών:** το engineered BAM-20 counterpart (2871.43) απέχει **1.09 Da**
από το native BAM-22 +2ox (2870.34). Χρειάζεται resolving power >2600 ή επιβεβαίωση με MS2,
αλλιώς θα διαβαστούν ως **μία** κορυφή.

### Χειρισμός δειγμάτων: όχι προαιρετικό
- **Εύρος σάρωσης 550–3100 Da** (η αρχική οδηγία ήταν 550–2900· επεκτείνεται για τα νέα species).
- **Untransfected + empty-vector controls**, ίδια σειρά και ίδιο passage, **κάθε φορά**.
- **Συμπεριλάβετε τα +16 oxidation satellites**, αλλιώς τα Met-πεπτίδια θα φαίνονται
  «χαμένα» ενώ έχουν μόνο οξειδωθεί. Ποσοτικοποιήστε **parent + sulfoxide ως ένα pool**.
- Συλλογή στον πάγο, άμεση οξίνιση (0.1% formic acid), αποφυγή freeze-thaw.

---

## 4. Παραδοτέο: αρνητικό αποτέλεσμα, Cycle 3b (και γιατί το λέμε)

Δοκιμάσαμε αν μια physics-based μέθοδος (MM-GBSA) μπορεί να **προβλέψει** δ/μ εκλεκτικότητα,
χρησιμοποιώντας **4 γνωστά** control πεπτίδια, όχι το engineered.

| Control | n | Υπολογισμένο ΔΔG | SEM | Πειραματικό |
|---|---|---|---|---|
| met-enkephalin | 5 | +26.38 | 1.46 | 0.00 |
| deltorphin I | 5 | +15.18 | 4.95 | +5.70 |
| deltorphin II | 5 | +7.48 | 3.24 | +5.39 |
| endomorphin-1 | 5 | −0.91 | 3.32 | −2.99 |

- **G1 PASS**: η κατεύθυνση/κατάταξη είναι σωστή.
- **G2′ FAIL**: μόνο η met-enkephalin περνά το όριο SEM 1.5 kcal/mol· οι άλλες 3.2–5.0.
- **G3 FAIL**: slope 0.594, 95% CI [−1.024, 2.213], r = 0.179. Το CI περιέχει το μηδέν.

**Ετυμηγορία: FAIL. Το Stage 2 δεν εγκρίνεται.** Άρα **κανένας υπολογιστικός ισχυρισμός για την
εκλεκτικότητα του `YGGFEVVG` δεν είναι έγκυρος.** Η μόνη έγκυρη οδός είναι **radioligand
competition binding**.

*Το αναφέρουμε επίτηδες. Η εναλλακτική (να παρουσιάσουμε μόνο το ένα control που πέρασε) θα
σας έστελνε σε ακριβό assay πάνω σε μέθοδο που δεν το στηρίζει.*

---

## 5. Τι πρέπει να γίνει: με σειρά προτεραιότητας

1. **ΤΩΡΑ, πριν φτάσουν τα πλασμίδια: παραγγείλετε το custom anti-`YGGFEVVG` polyclonal.**
   KLH-conjugated, ≥2 κουνέλια, **10–12 εβδομάδες** lead time. **Κανένα** εμπορικό
   anti-enkephalin αντίσωμα δεν αναγνωρίζει το `YGGFEVVG`: όλα είναι φτιαγμένα για το native
   πενταπεπτίδιο και τα περισσότερα χρειάζονται το ελεύθερο C-terminal Met. **Αυτό είναι το
   bottleneck όλου του expression readout.** Επιβεβαιώστε ότι ο immunogen είναι `YGGFEVVG` και
   όχι απλώς ο πυρήνας `YGGF`.
2. **Σύνθεση των 4 constructs** από το `PENK_order_sheet.csv`.
3. **Επεκτείνετε τη MS λίστα** με τα 4 species του cassette 5 (§3) και το εύρος στα 3100 Da.
4. **In vitro processing με recombinant ένζυμα**: όχι μόνο σε κύτταρα (§2).
5. **Radioligand binding** για `YGGFEVVG` και τη variant `YGGFDIIG` (§4).

---

## 6. Τι παραμένει ΑΝΟΙΧΤΟ: να το ξέρετε

- Τα engineered extended species `YGGFEVVGRGL` και `YGGFEVVGRF` **δεν έχουν δημοσιευμένη
  φαρμακολογία**. Είναι νέα, είναι αναμενόμενα, και πρέπει να **χαρακτηριστούν**, όχι να
  αφαιρεθούν με re-engineering.
- Το `YGGFEVVG` είναι **λιγότερο** σταθερό από τη native Met-enkephalin, όχι περισσότερο:
  3 θέσεις ευαίσθητες σε NEP έναντι 1. Η σταθερότητα της δελτορφίνης προέρχεται από
  **D-Ala** στη θέση 2, και τα D-αμινοξέα **δεν έχουν κωδικόνιο**: ένα ριβοσωμικά
  εκφρασμένο πεπτίδιο δεν μπορεί να το αναπαράγει. Κληρονομούμε το selectivity motif και
  **καθόλου** την αντοχή στις πρωτεάσες. Γι' αυτό το NEP-siRNA σκέλος είναι **κρίσιμο**, όχι
  συμπληρωματικό.
- **Ο πίνακας του cassette 5 (§3) είναι δικός μου υπολογισμός**, δεν έχει μετρηθεί ούτε
  ελεγχθεί από άλλον.

---

## Βιβλιογραφία

Όλα τα DOI επαληθεύτηκαν στο CrossRef.

1. Comb M et al. (1982). Primary structure of the human Met- and Leu-enkephalin precursor and its mRNA. *Nature* 295:663-666. doi:10.1038/295663a0
2. Noda M et al. (1982). Cloning and sequence analysis of cDNA for bovine adrenal preproenkephalin. *Nature* 295:202-206. doi:10.1038/295202a0
3. Stern AS et al. (1979). Isolation of the opioid heptapeptide Met-enkephalin [Arg6,Phe7]. *PNAS* 76:6680-6683. doi:10.1073/pnas.76.12.6680
4. Kilpatrick DL et al. (1981). Identification of the octapeptide [Met]enkephalin-Arg6-Gly7-Leu8. *BBRC* 103:698-705. doi:10.1016/0006-291x(81)90506-4
5. Matsuo H et al. (1983). Novel C-terminally amidated opioid peptide in human phaeochromocytoma tumour. *Nature* 305:721-723. doi:10.1038/305721a0
6. Boarder MR et al. (1985). Metorphamide, a C-terminally amidated opioid peptide. *Regulatory Peptides* 12:75-83. doi:10.1016/0167-0115(85)90184-3
7. Paquet L et al. (1996). Peptide biosynthetic processing: distinguishing PC1 and PC2. *Mol Cell Endocrinol* 120:161-168. doi:10.1016/0303-7207(96)03834-8
8. Fricker LD, Snyder SH (1982). Enkephalin convertase: purification and characterization. *PNAS* 79:3886-3890. doi:10.1073/pnas.79.12.3886
9. Eipper BA et al. (1992). The biosynthesis of neuropeptides: peptide alpha-amidation. *Annu Rev Neurosci* 15:57-85. doi:10.1146/annurev.neuro.15.1.57
10. Roques BP et al. (1980). The enkephalinase inhibitor thiorphan shows antinociceptive activity in mice. *Nature* 288:286-288. doi:10.1038/288286a0
11. Erspamer V et al. (1989). Deltorphins: naturally occurring peptides with high affinity and selectivity for delta opioid binding sites. *PNAS* 86:5188-5192. doi:10.1073/pnas.86.13.5188
12. Chavkin C, Goldstein A (1981). Specific receptor for the opioid peptide dynorphin: structure-activity relationships. *PNAS* 78:6543-6547. doi:10.1073/pnas.78.10.6543

**Πηγές δεδομένων:** UniProt P01210 (proenkephalin-A), UniProt P08473 (neprilysin/MME),
Human Protein Atlas cell-line RNA (nTPM, HEK293), GTEx v8.

**Αρχεία στο repo:** `04_plasmids/`, `07_invitro_penk/docs/PENK_INVITRO_PROTOCOL.md`,
`penk_ms_target_list.csv`, `06_engineering_cycles/cycle3b_physics_rescoring/docs/GATE_VERDICT_BOUND.md`,
`NATIVE_PENK_AMENDMENT2_WETLAB.md`, `dry_lab_modelling.md`
