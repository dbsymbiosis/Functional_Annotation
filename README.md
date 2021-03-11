# Functional_Annotation
Scripts to functionally annotate genes

Databases needed:
1. SwissProt (mmseq2 database formatted)
2. TrEMBL (mmseq2 database formatted)
3. PFAM_A
4. KOFAM

Programs needed:
1. mmseq2 (https://github.com/soedinglab/MMseqs2)
2. pfam_scan.pl (http://ftp.ebi.ac.uk/pub/databases/Pfam/Tools/PfamScan.tar.gz)
3. HMMER-3.1b2 (http://eddylab.org/software/hmmer/hmmer-3.1b2.tar.gz)
4. kofamscan (https://github.com/takaram/kofam_scan)

To run annotation:
1. Copy control script `run_FuncAnnot_MMseqs.sh` into your working directory
2. Change the specified variables within the script to those that are appropriate for your system (e.g. path to mmseq2, hmmer, etc.)
3. Run the script `./run_FuncAnnot_MMseqs.sh` to start the functional annotation process


