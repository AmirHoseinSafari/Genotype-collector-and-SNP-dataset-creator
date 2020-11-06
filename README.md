# genotypeCollector
Collecting Genotypes from ENA and make their SNPs

## dataCollector.py
In this code by using the Genotypes id in the "FILE_NAME".txt file we will download its .fastq files from ENA databese

## SNP.py
In this code by using the Genotypes id in the "FILE_NAME".txt file and its .fastq files we will make its SNP using bwa and samtools and GATK and get the common SNP of both files and store in ("Final_" + id + ".vcf")

If the code fail in make SNP of special Genotype, the id will be write in the "missIdForSNP.txt"

By calling preprocessing() function you will get the ( "Final_" + id + "_table.csv" ) file which contatin "pos, ref, alt" for each SNP

## tableCreatorGit.py
In this code we make a table for all the isolates

## sparseMatrix.py
Will store the table of tableCreatorGit.py in the sparse format to reduce size
