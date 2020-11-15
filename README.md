# genotypeCollector
In this code, we do the following thing:

1_ We download the .fastq files from ENA for each isolate.

2_ We find the SNPs for each isolate by using the bwa-mem and then samtools and GATK.

3_ We create a binary table. Each row represents an isolate and each column represents the SNP.

## dataCollector.py
In this code by using the isolate id in the "FILE_NAME".txt file we will download its .fastq files from ENA databese

## SNP.py
In this code by using the isolate id in the "FILE_NAME".txt file and its .fastq files we will find its SNP using bwa-mem and samtools and GATK and get the common SNP of both files and store in ("Final_" + id + ".vcf")

If the code fail in make SNP of special isolate, the id will be write in the "missIdForSNP.txt"

By calling preprocessing() function you will get the ( "Final_" + id + "_table.csv" ) file which contatin "pos, ref, alt" for each SNP

## tableCreatorGit.py
In this code we make a table for all the isolates

## sparseMatrix.py
Will store the table of tableCreatorGit.py in the sparse format to reduce size

---

## Citation
If you found the content of this repository useful, please cite us:

https://www.biorxiv.org/content/10.1101/2020.11.07.372136v1?rss=1

---
