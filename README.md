# genotypeCollector
In this code, we do the following things:

1_ We download the .fastq files from the european nucleotide archive (ENA) for each isolate.

2_ We find the SNPs for each isolate by using the bwa-mem and then samtools and GATK.

3_ We create a binary table. Each row represents an isolate and each column represents the SNP.

## dataCollector.py
In this code by using the isolate id in the "FILE_NAME".txt file we will download its .fastq files from the ENA database.

## SNP.py
In this code by using the isolate id in the "FILE_NAME".txt file and its .fastq files we will find its SNPs using bwa-mem and samtools and GATK and get the common SNPs of both files and store in ("Final_" + id + ".vcf").

If the code fails to find SNPs of special isolate, the id will be written in the "missIdForSNP.txt"

By calling preprocessing() function you will get the ( "Final_" + id + "_table.csv" ) file which contatin "pos, ref, alt" for each SNP of that isolate.

## tableCreatorGit.py
In this code, we create a binary table. Each row represents an isolate and each column represents the SNP.

## sparseMatrix.py
Will store the table of tableCreatorGit.py in the sparse format to reduce size.

---

## Citation
If you found the content of this repository useful, please cite us:

https://www.biorxiv.org/content/10.1101/2020.11.07.372136v2

---
